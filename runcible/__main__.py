import runcible
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Runcible is an application to orchestrate network device infrastructure"
    )
    parser.add_argument('--version', action='store_true')
    args = parser.parse_args()
    if args.version:
        print(runcible.__version__)
        exit(0)


if __name__ == '__main__':
    main()
