class ApiError(Exception):
  def __init__(self, response_object, *args: object) -> None:
    self.code = response_object.status_code
    try:
      json_response = response_object.json()
      self.message = json_response["message"]
    except:
      self.message = response_object.content.encode("UTF-8")

    super().__init__(*args)

  def __str__(self) -> str:
    return f"({self.code}) {self.message}"