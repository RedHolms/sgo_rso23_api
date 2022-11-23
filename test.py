import sgo_rso32_api as srapi

import sys

LOGIN = "leave here your login"
PASSWORD = "leave here your password"

def main():
  try:
    while True:
      try:
        session = srapi.Session()
        session.auth(LOGIN, PASSWORD)
        print("new auth")
      except KeyboardInterrupt: break
      except:
        print("exception: ", sys.exc_info()[1])
  except KeyboardInterrupt: pass

  return 0

if __name__ == "__main__":
  exit(main())