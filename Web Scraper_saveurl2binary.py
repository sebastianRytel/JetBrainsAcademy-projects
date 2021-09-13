import requests

def writing_to_file(page_content_request):
    file = open('source.html', 'wb')
    file.write(page_content_request)
    file.close()

def request_code(url):
    r = requests.get(url)
    if r:
        page_content_request = requests.get(url).content
        writing_to_file(page_content_request)
        return 'Content saved.'
    else:
        return f'The URL returned {r.status_code}!'

def main():
    print("Input the URL:")
    url = input()
    return request_code(url)

print(main())
