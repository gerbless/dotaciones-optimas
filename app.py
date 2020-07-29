import argparse
from app import create_app

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action',
                        help='determina  la acción a ejecutar [scheduling, generate, endowments, runerror]',
                        type=str)
    args = parser.parse_args()
    create_app(action=args.action)