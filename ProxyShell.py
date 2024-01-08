from shutil import copyfile
import requests
import socket

def is_bad_proxy(pip):    
	try:
		response = requests.get('http://ifconfig.me',
			proxies={
				"http": "socks5://" + pip,
				"https": "socks5://" + pip 
			},
			timeout=10
		)
	except requests.exceptions.Timeout:
		print('Timeout')
		return True
	except requests.exceptions.HTTPError as err:
		print("Http Error: ", err)
		return True
	except requests.exceptions.RequestException as e:
		print('Error code: ', e)
		return True
	return False

def good_proxy_list_maker(proxy_list):

	good_proxy_list = []

	for currentProxy in proxy_list:
		if is_bad_proxy(currentProxy):
			print("Bad Proxy %s" % (currentProxy))
		else:
			good_proxy_list.append(currentProxy)
			print("%s is working" % (currentProxy))

def main():
	socket.setdefaulttimeout(120)
	
	# Open Proxy list File
	proxy_list_f = open("./socks5.txt", "r")
	
	# Copy Proxy Conf
	new_proxy_conf_path = copyfile("./vierge_proxychains4.conf", "./new_proxychains4.conf")
	proxy_conf_f = open(new_proxy_conf_path, "a")
	
	# Formatting Proxy List
	proxy_text_list = proxy_list_f.read()
	proxy_text_list = good_proxy_list_maker(proxy_text_list.split("\n"))
	
	for i in proxy_text_list:
		i = i.split(":")
		i.insert(0, "socks5")
		proxy_conf_f.write(i[0] + "\t" + i[1] + "\t" + i[2] + "\n")

if __name__ == '__main__':
    main() 


	
