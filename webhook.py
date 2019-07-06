from flask import Flask, request, json
import json, os, subprocess

app = Flask(__name__)

local_repositories_path = input("Please input parent (upper) directory of repositories: ")

if os.path.isdir(local_repositories_path):
    print("Use input directory: ", local_repositories_path)
else:
    local_repositories_path= "/home/gao137/workspace/"
    print("Input error, use default directory: ", local_repositories_path)

@app.route('/')
def api_root():
   #data = json.loads(request.data)
   #print("New commit by: {}".format(data['commits'][0]['author']['name']))
    return "OK, Test successful"

@app.route('/github',methods=['POST'])

def api_wait_git_message():
    if request.headers['Content-Type'] == 'application/json':
        # get request
        request_info_json = request.json
        request_info = json.dumps(request_info_json)
        remote_repository_name = request_info_json["repository"]["name"]
        # not using since it ask for username and password
        remote_repository_path_html = request_info_json["repository"]["html_url"]
        remote_repository_path = request_info_json["repository"]["ssh_url"]
        #print("\n" + request_info)
        
        # assume a push initiated
        # 1. check if current repositories path contains this remote respository
        if remote_repository_name not in [f.name for f in os.scandir(local_repositories_path) if f.is_dir()]:
            # if not exist, clone
            print(remote_repository_name, "not exist in given local workspace , issue clone request")
            subprocess.call(['cd "' + local_repositories_path + '" && git clone '+ remote_repository_path], shell=True)
        else:
            current_local_repository_path = local_repositories_path + remote_repository_name
            # if exist, check if it is git repository
            if subprocess.call(['git', '-C', current_local_repository_path, 'status'], stderr=subprocess.STDOUT, 
                               stdout = open(os.devnull, 'w')) == 0:
                print(current_local_repository_path, " exist, issue pull request")
                # if it is git repository path
                subprocess.call(['cd "' + current_local_repository_path + '" && git pull '+ remote_repository_path],
                            shell=True)
            else:
                # if it is not git repository path
                user_input = input("Path exist, but it is not git repository, do you want to initiate directory as git repository (y) or exit the hook (n)?")
                if user_input in ["y","Y","YES","Yes","yes"]:
                    subprocess.call(['cd "' + current_local_repository_path + '" && git init '],shell=True)
                    subprocess.call(['cd "' + current_local_repository_path + '" && git pull ' + remote_repository_path],
                                    shell=True)
                else:
                    print("Exit the web hook for git auto synchronization")
                    func = request.environ.get('werkzeug.server.shutdown')
                    if func is None:
                        raise RuntimeError('Not running with the Werkzeug Server')
                    func()
                    
        return request_info

if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)
    #app.run()