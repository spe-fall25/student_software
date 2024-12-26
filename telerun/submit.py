#!/usr/bin/env python

import argparse
import urllib
import urllib.parse
import urllib.request
import ssl
import os
import json
import traceback
import time
import base64

timeout = 120 # seconds

DEBUG = False

server_cert = """
-----BEGIN CERTIFICATE-----
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
CRoJkaOmUioJ9OE=
-----END CERTIFICATE-----
"""

server_ip_port = "128.30.92.79:4443"
server_domain_name = "fatality.csail.mit.edu"
hidden_perf_directory = "/tmp/spe-student-jobs"

poll_interval = 1 # seconds

def process_response(response, script_args=None, job_id=None):
    result = json.loads(response["result"])["result_json"]
    if result["success"]:
        print("Job completed successfully.")
    else:
        print("Job failed.")
    print()
    print("--- Execution log:")
    print()
    print(result["execute_log"])
    
    if 'perf_data' in result and script_args:
        print()
        print("Perf data saved.")
        with open("perf.data", "wb") as f:
            f.write(base64.b64decode(result["perf_data"]))
        for idx, (orig_file, file) in enumerate(zip(script_args["orig_files"], script_args["files"])):
            if orig_file[:2] == './': 
                orig_file = orig_file[2:]
            with open(orig_file, 'rb') as f:
                orig_file_content = f.read()
                # write this to a hidden directory
                assert job_id is not None and script_args is not None
                # if job-{job_id} doesn't exist, create it
                if not os.path.exists(os.path.join(hidden_perf_directory, f"job-{job_id}")):
                    os.makedirs(os.path.join(hidden_perf_directory, f"job-{job_id}"))
                with open(os.path.join(hidden_perf_directory, f"job-{job_id}/{file}"), "wb") as f2:
                    f2.write(orig_file_content)
                    
    
def get_last_complete_job(username, token, ssl_ctx):
    query_params = {"username": username, "token": token}
    url_query = urllib.parse.urlencode(query_params)
    # url = "https://" + server_ip_port + "/api/last_complete?" + url_query
    url = "https://" + server_domain_name + "/api/submit?" + url_query
    req = urllib.request.Request(url, method="GET")
    try: 
        with urllib.request.urlopen(req, context=ssl_ctx) as f:
            response = json.load(f)
            if response["success"]:
                print("Last completed job:")
                process_response(response)
                if "perf_data" in response["result"]:
                    print("Can't retrieve perf data for last job.")
    except urllib.error.HTTPError as e:
        if e.code == 400:
            response_json = json.load(e)
            if response_json["error"] == "pending_job":
                return None
        else: 
            response_json = json.load(e)
            error = response_json.get("error", None)
            if error: 
                print("\n" + "=" * 50)
                print("ERROR:".center(50))
                print("-" * 50)
                print(error)
                print("=" * 50 + "\n")


def submit_job(username, token, script_args, ssl_ctx, override_pending=False, is_util=False):
    query_params = {"username": username, "token": token, "debug": int(DEBUG)}
    if override_pending:
        query_params["override_pending"] = "1"
    query_params["is_util"] = 1 if is_util else 0
    url_query = urllib.parse.urlencode(query_params)
    url = "https://" + server_ip_port + "/api/submit?" + url_query

    file_dict = set()
    for idx, file in enumerate(script_args["orig_files"]):
        with open(file, 'rb') as f:
            file_content = f.read()
            base64_encoded = base64.b64encode(file_content).decode("utf-8")
            script_args[f"file{idx}"] = base64_encoded
        script_args["files"].append(os.path.basename(file))
        if os.path.basename(file) not in file_dict:
            file_dict.add(os.path.basename(file))
        else:
            print(f"Duplicate file: {os.path.basename(file)}, please ensure all files are unique.")
            raise Exception("Duplicate file")
    req_json = json.dumps(script_args).encode("utf-8")
    request = urllib.request.Request(url, data=req_json, method="POST")
    request.add_header("Content-Type", "application/json")
    
    try:
        response = urllib.request.urlopen(request, context=ssl_ctx)
        response_json = json.load(response)
        return response_json["job_id"]
    except urllib.error.HTTPError as e:
        if e.code == 400:
            response_json = json.load(e)
            if response_json["error"] == "pending_job":
                return None
        else: 
            response_json = json.load(e)
            error = response_json.get("error", None)
            if error: 
                print("\n" + "=" * 50)
                print("ERROR:".center(50))
                print("-" * 50)
                print(error)
                print("=" * 50 + "\n")
        raise e
    
def preprocess_args(script_args):
    remaining_args = []
    files = []
    do_perf = False
    for idx, arg in enumerate(script_args):
        if idx == 0 and arg.startswith("perf"):
            assert script_args[idx + 1] == "record"
            do_perf = True

        if os.path.isfile(arg):
            remaining_args.append(f"file{len(files)}")
            files.append(arg)
        else:
            remaining_args.append(arg)
    returns = {
        "command": " ".join(remaining_args),
        "orig_files": files,
        "files": [],
        "perf": do_perf, 
    }
    return returns

def main():
    if DEBUG:
        print("DEBUG:", DEBUG)
    parser = argparse.ArgumentParser()
    # parser.add_argument('script_args', nargs=argparse.REMAINDER, help='Arguments for the script')
    parser.add_argument(
        "--auth",
        help="Authentication token (defaults to ./auth.json in the same directory as this script)",
        default=None
    )
    parser.add_argument(
        "--cores", 
        type=int,
        help="Number of cores to request",
        default=1
    )
    parser.add_argument("--username", type=str, help="Username", default="")
    parser.add_argument("--token", type=str, help="Token", default="")
    parser.add_argument("--override-pending", action="store_true", help="Allow overriding pending jobs")
    parser.add_argument("--utils", action="store_true", help="Use utility queue instead of main queue, for testing purposes instead of benchmarking performance. Timeout will be longer.")
    parser.add_argument("--bypass-last-job", action="store_true", help="Bypass checking for your last job.")
    args, script_args = parser.parse_known_args()
    if len(script_args) == 0:
        print("Please provide a script to run.")
        exit(1)
    
    # turn script_args into a dictionary 
    script_args = preprocess_args(script_args)
    script_args["cores"] = args.cores
    
    if args.username != "" and args.token != "":
        username = args.username
        token = args.token
    else:
        ## Check if auth token is valid
        token_path = f"{os.path.expanduser('~')}/.telerun/auth.json"
        if not os.path.isfile(token_path):
            if args.auth is None:
                print("Please provide an authentication token.")
                exit(1)
            if not os.path.isfile(args.auth):
                print("Invalid authentication token.")
                exit(1)
            if not os.path.exists(os.path.dirname(token_path)):
                os.system("mkdir -p " + os.path.dirname(token_path))   
            os.system(f"cp {args.auth} {token_path}")
            print("Authentication token copied to", token_path)
                
        ## Load auth token
        with open(token_path, "r") as f:
            auth = json.load(f)
        username = auth["username"]
        token = auth["token"]
    is_util = args.utils
    ssl_ctx = ssl.create_default_context(cadata=server_cert)

    if not args.bypass_last_job:
        last_complete_job = get_last_complete_job(username, token, ssl_ctx)

    job_id = submit_job(username, token, script_args, ssl_ctx, override_pending=args.override_pending, is_util=is_util)
    if job_id is None:
        print("You already have a pending job. Pass '--override-pending' if you want to replace it.")
        exit(1)
    print("Submitted job")

    already_claimed = False
    old_time = time.time()
    while True:
        
        if time.time() - old_time > timeout:
            print("Time limit exceeded.")
            break
        try:
            time.sleep(poll_interval)
                
            url_query = urllib.parse.urlencode({"username": username, "token": token, "job_id": job_id})
            req = urllib.request.Request(
                "https://" + server_ip_port + "/api/status?" + url_query,
                method="GET",
            )
            with urllib.request.urlopen(req, context=ssl_ctx) as f:
                response = json.load(f)
            
            state = response["state"]
            if state == "pending":
                continue
            elif state == "claimed":
                if not already_claimed:
                    print("Compiling and running, took {:.2f} seconds to be claimed.".format(time.time() - old_time)) 
                    already_claimed = True
                continue
            elif state == "complete":
                # TODO: Don't double-nest JSON!
                process_response(response, script_args=script_args, job_id=job_id) 
                
                req = urllib.request.Request(
                    "https://" + server_ip_port + "/api/reported?" + url_query,
                    method="POST",
                )    
                with urllib.request.urlopen(req, context=ssl_ctx) as f:
                    response = json.load(f)
                    print("Reported job completion.")
                    
                break
        except urllib.error.HTTPError as e:
            if e.code == 400:
                response_json = json.load(e)
                if response_json["error"] == "pending_job":
                    return None
            else: 
                response_json = json.load(e)
                error = response_json.get("error", None)
                if error: 
                    print("\n" + "=" * 50)
                    print("ERROR:".center(50))
                    print("-" * 50)
                    print(error)
                    print("=" * 50 + "\n")
            raise e
        except KeyboardInterrupt as e: 
            print("Keyboard Interrupted.")
            if not already_claimed: 
                url_query = urllib.parse.urlencode({"username": username, "token": token, "job_id": job_id})
                req = urllib.request.Request(
                    "https://" + server_ip_port + "/api/delete?" + url_query,
                    method="POST",
                )
                with urllib.request.urlopen(req, context=ssl_ctx) as f:
                    response = json.load(f)
                    if response["success"]:
                        print("Job removed successfully.")
            break
        except Exception as e:
            traceback.print_exc()
            continue

if __name__ == "__main__":
    os.makedirs(hidden_perf_directory, exist_ok=True)
    main()
