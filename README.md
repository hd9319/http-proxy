# http-proxy
Extends the Python requests library by adding additional options for proxy/user agent rotation as well as tracking.

## Prerequisites
* Requires the requests library
* Requires two .txt files: one which contains a list of webpages with proxies and the other with a list of user agents

## Installing
1. Create a virtual environment for your project and activate
`virtualenv -p python3 [projectname]`

2. Clone repository
`git clone https://github.com/hd9319/http-proxy`

3. Install dependencies using requirements.txt files
`pip install -r requirements.txt`

## How to Use
1. Import ProxyRequest class into any project and use in place of requests library.
2. Instantiate class and pass in parameters for retrieving list of user agents and proxies
3. Refresh proxies before running any type of requests
4. request() method returns a dictionary containing a response object, headers and proxy ip used for making the call.
`from proxy import ProxyRequest

proxy_urls_path = 'C/.../*.txt'
user_agents_path = 'C/.../*.txt'

requests = ProxyRequest(proxy_urls_path, user_agents_path, timer=0)
               acceptable_status_codes=[200])
_ = requests.refresh_proxies()
response = requests.request(request, headers)
`
