import os
import sys
import json

def generate_buildspec(changed_files):
    lambda_function_dirs = set()

    # Identify all modified Lambda function directories
    for file in changed_files:
        if file.startswith("lambda-functions/") and file.endswith("/index.py"):
            lambda_function_dirs.add(os.path.dirname(file))

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
                "commands": []
            }
        }
    }

    # Add deployment commands only for modified functions
    if lambda_function_dirs:
        for lambda_function_dir in lambda_function_dirs:
            function_name = os.path.basename(os.path.dirname(lambda_function_dir))
            buildspec["phases"]["build"]["commands"].extend([
                f"echo 'Deploying {function_name} Lambda Function'",
                f"cd {lambda_function_dir}",
                f"zip {function_name}.zip index.py",
                f"aws lambda update-function-code --function-name {function_name} --zip-file fileb://{function_name}.zip",
                f"aws lambda update-function-configuration --function-name {function_name} --layers ${function_name.upper()}_ARN",
                "cd -"
            ])
    else:
        # Create a dummy buildspec to prevent CodeBuild failure
        buildspec["phases"]["build"]["commands"].append("echo 'No Lambda function changes detected.'")

    return json.dumps(buildspec, indent=2)

if __name__ == "__main__":
    changed_files = sys.argv[1:]
    buildspec_content = generate_buildspec(changed_files)
    with open("buildspec.yml", "w") as f:
        f.write(buildspec_content)
