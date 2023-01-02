from typing import Tuple

from nostr.key import PrivateKey


def generate_keys() -> Tuple[str, str]:
    private_key = PrivateKey()
    public_key = private_key.public_key
    return private_key, public_key


def vanity_key(prefix:str='', suffix:str='', limit:int=1000000,
               use_hex:bool=False) -> Tuple[str, str]:
    
    if not prefix and not suffix:
        print('Error: please enter a desired prefix and/or suffix')
        return None, None
    elif len(prefix + suffix) >= 10:
        print('Error: vanity string too long, prefix+suffix must be < 10 chars')
        return None, None
    
    hex_chars = '0123456789abcdef'
    bech32_chars = 'qpzry9x8gf2tvdw0s3jn54khce6mua7l'
    if use_hex:
        char_set = hex_chars
        msg_type = 'hex'
        if prefix:
            prefix_start, prefix_end = None, len(prefix)
    else:
        char_set = bech32_chars
        msg_type = 'bech32'
        # Account for leading chars 'npub1' before prefix in bech32
        if prefix:
            prefix_start, prefix_end = 5, len(prefix)+5
    if suffix:
        suffix_start, suffix_end = (-1)*len(suffix), None
        
    if not all(c in set(char_set) for c in set(prefix + suffix)):
        print(f"Error: vanity string must only contain {msg_type} characters: '{char_set}'")
        return None, None
    
    print(f'Generating vanity {msg_type} public key with:')
    if prefix:
        print(f"  Prefix: '{prefix}'")
    if suffix:
        print(f"  Suffix: '{suffix}'")
    print(f'Will make {limit} attempts...', '\n')
    for i in range(1, limit+1):
        private_key, public_key = generate_keys()
        test_key = public_key.hex() if use_hex else public_key.bech32()
        prefix_match = False if prefix else True
        suffix_match = False if suffix else True
        if not prefix_match:
            if test_key[prefix_start:prefix_end] == prefix:
                prefix_match = True
        if not suffix_match:
            if test_key[suffix_start:suffix_end] == suffix:
                suffix_match = True
        if prefix_match and suffix_match:
            print('\n', f'Match on {i}th attempt!')
            print(f'Public key: {test_key}')
            return private_key, public_key
        elif i % 100000 == 0:
            print(f'Attempt {i}')
    
    print('\n', f'Could not find a vanity key in {i} attempts :(')
    return None, None


# Run program:
# private_key, public_key = vanity_key(prefix='58k', suffix='58k', limit=1000000)
