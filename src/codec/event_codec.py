from __future__ import annotations
import os
from src.common.enums.deployment_environment import DeploymentEnvironment
from src.common.enums.serialization_format import SerializationFormat
from src.common.enums.encryption_scheme import EncryptionScheme
from src.common.models.sensor_event import SensorEvent
from src.common.crypto.cipher.aes_gcm_cipher import AesGcmCipher
from src.common.crypto.cipher.base import PayloadCipher
from src.common.crypto.cipher.chacha20_poly1305_cipher import ChaCha20Poly1305Cipher
from src.common.crypto.cipher.no_encryption_cipher import NoEncryptionCipher
from src.common.serialization.base import PayloadSerializer
from src.common.serialization.serializers.json.json_serializer import JsonSerializer
from src.common.serialization.serializers.protobuf.protobuf_serializer import ProtobufSerializer

_ENV_CIPHER_KEY = "PIPELINE_CIPHER_KEY"

class InsecureCodecError(Exception):
    """Raised at startup when the active codec does not meet environment security requirements."""

class EventCodec:
    """Composes serialization and encryption into a single encode/decode operation."""

    def __init__(
        self,
        serializer: PayloadSerializer,
        cipher:     PayloadCipher,
        env:        DeploymentEnvironment,
    ) -> None:
        self._serializer = serializer
        self._cipher     = cipher
        self._env        = env
        self._enforce_production_requirements()

    def _enforce_production_requirements(self) -> None:
        _SECURE_CIPHERS = {EncryptionScheme.AES_GCM, EncryptionScheme.CHACHA20_POLY1305}
        errors: list[str] = []

        if self._env.requires_structured_serialization() and self._serializer.format != SerializationFormat.PROTOBUF:
            errors.append(
                f"Serializer must be PROTOBUF in {self._env.value}, "
                f"got '{self._serializer.format.value}'. "
                "Protobuf reduces payload size and enforces schema."
            )
        if self._env.requires_encryption() and self._cipher.scheme not in _SECURE_CIPHERS:
            errors.append(
                f"Cipher must be AES_GCM or CHACHA20_POLY1305 in {self._env.value}, "
                f"got '{self._cipher.scheme.value}'. "
                "Sensor data must never travel unencrypted."
            )

        if errors:
            raise InsecureCodecError(
                f"Codec does not meet {self._env.value} security requirements:\n"
                + "\n".join(f"  [{i + 1}] {e}" for i, e in enumerate(errors))
            )

    def encode(self, event: SensorEvent) -> bytes:
        return self._cipher.encrypt(self._serializer.serialize(event))

    def decode(self, data: bytes) -> SensorEvent:
        return self._serializer.deserialize(self._cipher.decrypt(data))

    @property
    def encoding(self) -> str:
        return self._serializer.format.value

    @property
    def cipher_scheme(self) -> str:
        return self._cipher.scheme.value

class EventCodecFactory:
    """Builds an EventCodec from pipeline.yaml codec/cipher string values."""

    @staticmethod
    def create(
        codec: str = "json",
        cipher: str = "none",
        env: DeploymentEnvironment | None = None,
    ) -> EventCodec:
        if env is None:
            env = DeploymentEnvironment.parse(
                os.getenv("DEPLOYMENT_ENVIRONMENT", "simulation")
            )
        return EventCodec(
            serializer=EventCodecFactory._build_serializer(SerializationFormat.parse(codec)),
            cipher=EventCodecFactory._build_cipher(EncryptionScheme.parse(cipher)),
            env=env,
        )

    @staticmethod
    def _build_serializer(format: SerializationFormat) -> PayloadSerializer:
        match format:
            case SerializationFormat.JSON:
                return JsonSerializer()
            case SerializationFormat.PROTOBUF:
                return ProtobufSerializer()

    @staticmethod
    def _build_cipher(scheme: EncryptionScheme) -> PayloadCipher:
        match scheme:
            case EncryptionScheme.NO_ENCRYPTION:
                return NoEncryptionCipher()
            case EncryptionScheme.AES_GCM:
                return AesGcmCipher(EventCodecFactory._require_key())
            case EncryptionScheme.CHACHA20_POLY1305:
                return ChaCha20Poly1305Cipher(EventCodecFactory._require_key())

    @staticmethod
    def _require_key() -> str:
        key = os.getenv(_ENV_CIPHER_KEY)
        if not key:
            raise RuntimeError(
                f"{_ENV_CIPHER_KEY} is not set. "
                "Required when pipeline.cipher is aes_gcm or chacha20_poly1305.\n"
                f"Generate: python -c \"import secrets; print(secrets.token_hex(32))\""
            )
        return key
