# utils/messages.py

# Success messages
LOGIN_SUCCESS = "Đăng nhập thành công!"
REGISTER_SUCCESS = "Đăng ký tài khoản mới thành công!"
DELETE_SUCCESS = "Xóa {object} thành công!"
UPDATE_SUCCESS = "Cập nhật {object} thành công!"
CREATE_SUCCESS = "Tạo {object} mới thành công!"
GET_SUCCESS = "Lấy danh sách {object} thành công!"
GET_DETAIL_SUCCESS = "Lấy thông tin {object} thành công!"
LOGOUT_SUCCESS = "Đăng xuất thành công!"
REFRESH_TOKEN_SUCCESS = "Làm mới access token thành công!"

CREATE_ERROR = "Tạo {object} không thành công!"
UPDATE_ERROR = "Cập nhập {object} không thành công!"
DELETE_ERROR = "Xóa {object} không thành công!"
GET_ERROR = "Lấy danh sách {object} không thành công!"
GET_DETAIL_ERROR = "Lấy thông tin {object} không thành công!"

# Error messages
INVALID_DATA = "Dữ liệu không hợp lệ."
NOT_FOUND = "Không tìm thấy {object}."
SERVER_ERROR = "Lỗi hệ thống, vui lòng thử lại sau."
UNAUTHORIZED = "Không có quyền truy cập."
INVALID_TOKEN = "Token không hợp lệ hoặc đã hết hạn."

LOGIN_FAIL = "Tên đăng nhập hoặc mật khẩu không đúng."
USER_NOT_FOUND = "Tài khoản không tồn tại."
PASSWORD_INCORRECT = "Mật khẩu không đúng."
ACCOUNT_DISABLED= "Tài khoản đã bị vô hiệu hóa."