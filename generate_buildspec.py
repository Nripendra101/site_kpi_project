import os
import sys
import json

def generate_buildspec(changed_files):
    lambda_function_dir = None
    for file in changed_files:
        if file.startswith("lambda-functions/") and file.endswith("/index.py"):
            lambda_function_dir = os.path.dirname(file)
            break

    if not lambda_function_dir:
        print("No Lambda function changes detected.")
        return None

    function_name = os.path.basename(os.path.dirname(lambda_function_dir))

    buildspec = {
        "version": "0.2",
        "phases": {
            "install": {
                "runtime-versions": {
                    "python": "3.11"
                }
            },
            "pre_build": {
                "commands": [
                    "source ./build_env.sh"
                ]
            },
            "build": {
                "commands": [
                    f"echo 'Deploying {function_name} Lambda Function'",
                    f"cd {lambda_function_dir}",
                    f"zip {function_name}.zip index.py",
                    f"aws lambda update-function-code --function-name {function_name} --zip-file fileb://{function_name}.zip",
                    f"aws lambda update-function-configuration --function-name {function_name} --layers ${function_name.upper()}_ARN",
                ]
            }
        }
    }
    return json.dumps(buildspec, indent=2)

if __name__ == "__main__":
    changed_files = sys.argv[1:]
    buildspec_content = generate_buildspec(changed_files)
    if buildspec_content:
        with open("buildspec.yml", "w") as f:
            f.write(buildspec_content)