# code-webhook
A simple python webhook try to updated local repository automatically on each Github push (or other event base on you setting).

To set it up, do the following:

1. install python, flask, ngrok
2. set up ngrok (https://ngrok.com/) it is used to review you localhost server to outside world
3. run `python webhook.py` it should ask you for parent directory of repositories. After you type in you parent directory of repositories, it will try to start up a local flask server, remember the [port] number on this local machine
4. run `ngrok http [port]` it should instantly create a public HTTPS URL for a web site running locally on your development machine. Now remember the public HTTPS URL for github hook.
5. Next is to set webhook with github, here is tutorial on how to set it up: 
[https://developer.github.com/webhooks/creating/](https://developer.github.com/webhooks/creating/) 
---
6. Now you need to set up ssh key
   - 6.1 You can either add ssh key for all repository, here is tutorial on how to set it up : [https://help.github.com/en/enterprise/2.16/user/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent](https://help.github.com/en/enterprise/2.16/user/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) 
   - 6.2 or use github deploy key, here is tutorial on how to use deploy key: [https://gist.github.com/zhujunsan/a0becf82ade50ed06115](https://gist.github.com/zhujunsan/a0becf82ade50ed06115) 
7. now everything should be up and running now, to put process to background, you can use `screen` command
