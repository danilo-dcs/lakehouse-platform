import sys


class ArgsHandler:
    def parse_gcs(self, args: list) -> dict:
        if len(args) - 1 != 4:
            print("""
                Usage: \n 
                spark-submit --jar <location>.json --packages io.delta:delta-spark_2.12:3.1.0 src/shared/spark/spark_script.py arg1 arg2 agr3 arg4 arg5 arg6 \n
                arg1 -> 'bucket_name'\n
                arg2 -> 'collection'\n
                arg3 -> 'private_key_id'\n
                arg4 -> 'private_key_token'\n
                arg5 -> 'service_account_email'\n
                arg6 -> file_names: '[file1, file2, ..., filen]'\n
            """)
            sys.exit(1)
        return dict(
            bucket_name=args[1],
            collection=args[2],
            private_key_id=args[3],
            private_key_token=args[4],
            service_account_email=args[5],
            files=args[6],
        )
