def log_warn(message: str):
  print(f"⚠️ \033[33m{message}\033[0m")

def log_error(message: str):
  print(f"❌ \033[31m{message}\033[0m")

def log_success(message: str):
  print(f"✅ \033[32m{message}\033[0m")

def log_info(message: str):
  print(f"ℹ️ \033[34m{message}\033[0m")
