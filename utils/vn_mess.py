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
#Thông báo dành cho lọc ngày
FOUND_TRIPS_BY_DATE = "Tìm thấy {count} chuyến đi trong ngày {date}"
FOUND_TRIPS_BY_TIME_ON_DAY = "Tìm thấy {count} chuyến đi trong khoảng thời gian {start_time} ngày {date}"
MISSING_PARAM = "Thiếu tham số {params}"
INVALID_DATE = "Ngày không hợp lệ"
INVALID_DATE_TIME_FORMAT = "Định dạng ngày hoặc giờ không hợp lệ"
FOUND_TRIPS_BY_ROUTE = "Tìm thấy {count} chuyến đi theo tuyến có mã {route_id}"
CREATED_MULTIPLE_TRIPS = "Tạo thành công {count} chuyến đi từ {start_date} đến {end_date} lúc {time}"

START_DATE_GREATER_THAN_END_DATE = "Ngày bắt đầu phải nhỏ hơn hoặc bằng ngày kết thúc"
INVALID_ACTIVE = "Trường is_active phải là kiểu boolean."
BUSY = "Tài xế hoặc xe đã bận trong khoảng thời gian này."
INVALID_ROUTE_LOCATION = "Tài xế và xe hiện đang ở {current_location}, không thể khởi hành từ {departure_location}."
START = "Đã xuất phát"

# Vé
NOT_DELETE_TICKET_INVOICE = "Không thể xoá vé đã có hoá đơn."