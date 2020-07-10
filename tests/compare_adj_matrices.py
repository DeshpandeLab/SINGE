import argparse
import numpy as np
import sys
from hdf5storage import loadmat

def main(args):
    '''
    Compare two sparse matrices stored in .mat files.
    Each .mat file is expected to have the sparse matrix stored in Adj_Matrix.
    Uses numpy.allclose to compare the data values using the specified tolerance.
    Return with exit code 1 if the spare matrices are not equal.
    '''
    # This version of loadmat supports HDF5-formatted MAT files from
    # MATLAB version 7.3 and falls back on the scipy.io.loadmat to read
    # earlier versions of MAT files.
    # However, the version 7.3 and older MAT file format use different data
    # structures to store sparse matrices.
    mat_contents1 = loadmat(args.mat_file[0])
    matrix1 = mat_contents1['Adj_Matrix']

    mat_contents2 = loadmat(args.mat_file[1])
    matrix2 = mat_contents2['Adj_Matrix']

    # Inspired by PyPardisoProject
    # https://github.com/haasad/PyPardisoProject/blob/f666ea4718b32fa1359e5ca94bedac710b09a428/pypardiso/pardiso_wrapper.py#L173
    if not (np.array_equal(matrix1['jc'], matrix2['jc']) and 
            np.array_equal(matrix1['ir'], matrix2['ir'])):
        print('Spare matrices in {} and {} have different nonzero elements'.format(args.mat_file[0],
              args.mat_file[1]))
        sys.exit(1)

    if not np.allclose(matrix1['data'], matrix2['data'], args.rtol, args.atol):
        print('Spare matrices in {} and {} have different values'.format(args.mat_file[0],
              args.mat_file[1]))
        max_diff = max(max(np.abs(matrix1['data'] - matrix2['data'])))
        print('Maximum absolute difference: {}'.format(max_diff))
        sys.exit(1)

    print('Spare matrices in {} and {} are equal'.format(args.mat_file[0],
          args.mat_file[1]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compare the Adj_Matrix '
        'sparse matrices in two .mat files. '
        'Return with exit code 1 if they are not equal.')
    parser.add_argument('mat_file', type=str, nargs=2,
                        help='The .mat files to compare. Exactly two required.')
    # Display defaults per https://stackoverflow.com/questions/12151306/argparse-way-to-include-default-values-in-help/18507871#18507871
    parser.add_argument("--rtol", type=float, default=1e-05,
                        help='The relative tolerance parameter for numpy.allclose (default: %(default).2e)')
    parser.add_argument("--atol", type=float, default=1e-08,
                        help='The absolute tolerance parameter for numpy.allclose (default: %(default).2e)')

    main(parser.parse_args())
