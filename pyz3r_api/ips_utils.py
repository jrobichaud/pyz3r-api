# from: https://gist.github.com/sli/23b6ffe3b2533e87d42e27c12d964565


def get_uint16(data, index):
    return int((data[index] << 8) | data[index + 1])


def get_uint24(data, index):
    return int((data[index] << 16) | (data[index + 1] << 8) | data[index + 2])


def patch_with_ips(file_data, patch_data):
    i = 5
    while i < len(patch_data) - 3:
        # Get offset
        offset = get_uint24(patch_data, i)
        i += 3

        # Get packet size
        size = get_uint16(patch_data, i)
        i += 2

        # Check & apply
        if size == 0:
            # Get RLE repeat count
            rle_size = get_uint16(patch_data, i)
            i += 2

            # Get repeat byte
            repeat = patch_data[i]
            i += 1

            # Apply to file
            for x in range(rle_size):
                file_data[offset + x] = repeat
        else:
            # Normal packet
            # Copy from patch to file
            for x in range(size):
                file_data[offset + x] = patch_data[i]
                i += 1
