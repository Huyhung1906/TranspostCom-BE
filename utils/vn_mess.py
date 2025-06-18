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

# Hóa đơn
# utils/vn_mess.py

INVOICE_CREATE_SUCCESS = "Tạo hóa đơn thành công."
INVOICE_LIST_SUCCESS = "Lấy danh sách hóa đơn thành công."
INVOICE_DETAIL_SUCCESS = "Lấy chi tiết hóa đơn thành công."
INVOICE_CREATE_NO_TICKETS = "Vui lòng chọn ít nhất một vé để tạo hóa đơn."
INVOICE_CREATE_TICKET_INVALID = "Không tìm thấy vé hợp lệ để tạo hóa đơn."

PAYMENT_CREATE_SUCCESS = "Tạo giao dịch thanh toán thành công."
PAYMENT_LIST_SUCCESS = "Lấy danh sách giao dịch thanh toán thành công."
NO_VALID_TICKETS="Không giá trị"

NO_SELECT = "Bạn chưa chọn ghế nào."
SEAT_NOT_AVAILABLE = "Một số vé đã được giữ hoặc bán."
SUCCESS_HOLD_SEAT = "Giữ vé thành công. Vui lòng thanh toán trong 20 phút."
SUCCESS_RELEASE_SEAT ="Huỷ giữ vé thành công."

LACK_INFO = "Thiếu thông tin để tạo hóa đơn."
SEAT_DEFIRENT_PESS ="Số lượng hành khách không khớp với số vé."
SEAT_NOT_TRUE = "Vé không hợp lệ hoặc đã được thanh toán."

LACK_ID_INVOICE = "Thiếu mã hóa đơn."
URL_SUCCESS ="Tạo URL thanh toán thành công."

LACK_INFO_INVOICE ="Vui lòng cung cấp mã hóa đơn hoặc mã vé."