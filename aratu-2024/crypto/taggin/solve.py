from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.x963kdf import X963KDF

public_key="ec838de0b7e267570193785a527ace9c55db4f9649c0c2bf9f42aedd"

private_key=0xf37893f64e6c75a82a05678823fca9ff1a3fc7e5e2790eb610300104
symmetric_key="b8130f84d0cc7cfd0bddcf06f96a3ce4b3c3c3877360a86524a37f226d2ac352"


sk_i = bytes.fromhex(symmetric_key)
for i in range(6):
    kdf_update = X963KDF(
            algorithm=hashes.SHA256(),
            length=32,
            sharedinfo=sk_i
            )

    sk_i = kdf_update.derive(b"update")

    kdf_diversify = X963KDF(
            algorithm=hashes.SHA256(),
            length=72,
            sharedinfo=sk_i
            )
    anti_tracking = kdf_diversify.derive(b"diversify")
    u_i, v_i = anti_tracking[:36], anti_tracking[36:],

    u_i = int(u_i.hex(), 16)
    v_i = int(v_i.hex(), 16)

    d_i = (private_key * u_i) + v_i
    print(hex(d_i))
