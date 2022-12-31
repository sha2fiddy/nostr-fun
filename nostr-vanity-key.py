from nostr.key import PrivateKey


def generate_keys():
    private_key = PrivateKey()
    public_key = private_key.public_key
    return private_key, public_key


def vanity_address(prefix, use_hex=False, limit=1000000):
    
    hex_chars = '0123456789abcdef'
    bech32_chars = 'qpzry9x8gf2tvdw0s3jn54khce6mua7l'
    if use_hex:
        char_set = hex_chars
        start, end = 0, len(prefix)
        msg_type = 'hex'
    else:
        char_set = bech32_chars
        start, end = 5, len(prefix)+5
        msg_type = 'bech32'
    if not all(c in char_set for c in prefix):
        print(f"Error: prefix must only contain {msg_type} characters: '{char_set}'")
        return None, None
    
    print(f"Generating vanity {msg_type} public key with prefix: '{prefix}'...", '\n')
    for i in range(limit):
        private_key, public_key = generate_keys()
        test_key = public_key.hex() if use_hex else public_key.bech32()
        if test_key[start:end] == prefix:
            print(f'Match on {i}th attempt!')
            print(f'Public key: {test_key}')
            return private_key, public_key
        
    print(f'Could not find a vanity address in {str(limit)} attempts :(')
    return None, None


# Run program:
# private_key, public_key = vanity_address(prefix='b00b', use_hex=True, limit=100000)