import sys
import re
import urllib.request


class QueryTester:
    def __init__(self):
        self.urls = []

    def add_url(self, url):
        if self.validate_url(url):  # Makes sure the url is a valid url.
            self.urls.append(url)

    @staticmethod
    def validate_url(url):
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if re.match(regex, url) is not None:
            return True
        else:
            return False

    def run_query(self, url_index):
        if 0 <= url_index < len(self.urls):
            try:
                response = urllib.request.urlopen(self.urls[url_index])
                return str(response.read())
            except:  # The request encountered an exception.
                return ""
        else:  # The provided index was out of bound.
            return ""


def main():
    query_tester = QueryTester()
    max_args = 2

    if len(sys.argv) > max_args:  # Limits the amount of arguments.
        print("Too many arguments.")
        return  # Exit the program.
    elif len(sys.argv) == max_args:  # Checks to see if the url is valid.
        if query_tester.validate_url(sys.argv[1]):
            query_tester.add_url(sys.argv[1])  # Append the url.
            print("The url was successfully added.")
        else:
            print("Invalid url.")
            return  # Exit the program.

    while True:
        user_input = input("Enter Command (help, a, r, q): ")
        if user_input == "q":
            return
        elif user_input == "help":
            print("Type 'a' to add a url to your list of urls.")
            print("Type 'r' to run a get request on a url.")
            print("Type 'q' to exit the program.")
        elif user_input == "a":
            attempts = 3
            while attempts > 0:  # 3 attempts for user to enter a valid url, otherwise return to main interface.
                user_input = input("Enter url: ")
                if query_tester.validate_url(user_input):  # Validates url format.
                    query_tester.add_url(user_input)  # Appends url.
                    print("The url was successfully added.")
                    break
                else:
                    attempts-=1
                    print("The url is invalid, "+str(attempts)+" attempts remaining.")
        elif user_input == "r":
            if len(query_tester.urls) > 0:  # Makes sure the url list isn't empty.
                print("List of urls: ")
                for i in range(len(query_tester.urls)):  # Prints all urls.
                    print(str(i+1) + ". "+query_tester.urls[i])
                user_input = input("Type the number that corresponds to the url you want to query: ")
                try:
                    url_index = int(user_input)
                    if 0 < url_index <= len(query_tester.urls):
                        content = query_tester.run_query(url_index-1)
                        print("\nContent:\n"+content+"\n")
                    else:  # Out of bound index.
                        print("The value is out of range.")
                except ValueError:  # The user didn't enter a number.
                    print('Invalid input.')
            else:  # There's nothing to run.
                print("List of urls is empty.")


if __name__ == '__main__':
    main()
