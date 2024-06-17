import os
import pandas as pd
import numpy as np

# Đọc File
def read_file(file_name):
    try:
        # Kiểm tra sự tồn tại của File
        if os.path.exists(file_name):
            print('File tồn tại, đang tiến hành đọc File.')
            # Mở, đọc file
            with open(file_name, 'r') as file:
                # Đọc tất cả các dòng lưu vào list data
                data = file.readlines()
            # Trả về nội dung đã đọc
            return data
        # File không có, in thông báo
        else:
            print('File không tồn tại. Vui lòng kiểm tra lại tên File và thử lại.')
            return None
    # Nếu xảy ra lỗi, in thông báo
    except Exception as e:
        print(f'Có lỗi xảy ra: {e}')
        return None

# Kiểm tra và phân loại dữ liệu
def validate_data(data):
    # list lưu trữ các dòng dữ liệu hợp lệ
    valid_lines = []
    # biến đếm các dòng dữ liệu không hợp lệ
    invalid_lines = 0
    # Vòng lặp FOR kiểm tra từng dòng dữ liệu trong list data
    for line in data:
        # loại bỏ khoảng trắng ở đầu và cuối dòng
        line = line.strip()
        # tách dòng dựa theo dấu phẩy
        parts = line.split(',')
        # Kiểm tra các tiêu chí để xác định dữ liệu có hợp lệ hay không:
        # len(parts) == 26 --> Dòng phải chứa đúng 26 phần sau khi tách
        # parts[0].startswith('N') --> Phần đầu tiên của dòng phải bắt đầu bằng chữ 'N'
        # len(parts[0]) == 9 --> Phần đầu tiên của dòng phải có độ dài là 9 ký tự
        # parts[0][1:].isdigit() --> Các ký tự từ thứ 2 đến thứ 9 của phần đầu tiên phải là số
        if len(parts) == 26 and parts[0].startswith('N') and len(parts[0]) == 9 and parts[0][1:].isdigit():
            # Thêm dòng hợp lệ vào list lưu trữ
            valid_lines.append(parts)
        else:
            # Nếu dòng không hợp lệ, tăng biến đếm thêm 1
            invalid_lines += 1
            # In dòng dữ liệu không hợp lệ
            print(f'Dữ liệu không hợp lệ: {line}')
    # In thống kê
    print(f'Tổng số dòng dữ liệu hợp lệ: {len(valid_lines)}')
    print(f'Tổng số dòng dữ liệu không hợp lệ: {invalid_lines}')
    # Trả về list các dòng dữ liệu hợp lệ
    return valid_lines

# Chấm điểm
def grade_exams(valid_data, answer_key):
    # Chuyển chuỗi đáp án thành list mỗi phần tử là đáp án của 1 câu hỏi
    answer_key = answer_key.split(',')
    # list scores lưu trữ điểm số của mỗi học sinh
    scores = []
    # Vòng lặp FOR lấy từng dòng câu trả lời của sinh viên trong list dữ liệu hợp lệ
    for student_answers in valid_data:
        # Tạo biến điểm
        score = 0
        # hàm zip(student_answers[1:], answer_key) ghép cặp từng phần tử câu trả lời của sinh viên với từng phân tử của đáp án
        # Vòng lặp FOR chạy từng cặp phần tử câu trả lời của sinh viên và đáp án tương ứng với từng câu hỏi
        for answer, correct_answer in zip(student_answers[1:], answer_key):
            if answer == correct_answer: # Nếu sinh viên trả lời đúng
                score += 4
            elif answer == '': # Nếu sinh viên không trả lời
                score += 0
            else: # Nếu sinh viên trả lời sai
                score -= 1
        # Vòng lặp FOR kết thúc, điểm từng câu trả lời được thêm vào list scores
        scores.append(score)
    return scores

# Thống kê điểm
def calculate_statistics(scores):
    # Sử dụng thư viện NumPy để tính toán, thống kê điểm số
    # Chuyển list scores thành mảng NumPy
    # Sử dụng các hàm sum(), mean(), max(), min(), median() để tính toán số liệu thống kê
    scores = np.array(scores)
    high_scores = np.sum(scores > 80)
    average_score = np.mean(scores)
    max_score = np.max(scores)
    min_score = np.min(scores)
    range_of_scores = max_score - min_score
    median_score = np.median(scores)
    # In các số liệu thống kê
    print(f'Số lượng học sinh đạt điểm cao (>80): {high_scores}')
    print(f'Điểm trung bình: {average_score:.3f}')
    print(f'Điểm cao nhất: {max_score}')
    print(f'Điểm thấp nhất: {min_score}')
    print(f'Miền giá trị của điểm: {range_of_scores}')
    print(f'Giá trị trung vị: {median_score:.3f}')

# Ghi File
def save_results_file(original_file_name, valid_data, scores):
    # Tên File lưu kết quả thêm chuỗi '_grades'
    results_file_name = original_file_name.replace('.txt', '_grades.txt')
    # Tạo/Ghi đè file lưu kết quả (chế độ ghi)
    with open(results_file_name, 'w') as file:
        # hàm zip(valid_data, scores) ghép cặp student_id trong valid_data với điểm số trong scores
        for student_id, score in zip(valid_data, scores):
            # Vòng lặp FOR chạy từng cặp phần tử do hàm zip() tạo ra để ghi lần lượt vào File lưu kết quả
            file.write(f'{student_id[0]},{score}\n')
    # In thông báo sau khi hoàn thành việc ghi vào file lưu kết quả
    print(f'Kết quả đã được lưu vào tệp: {results_file_name}')

# Chạy chương trình
def main():
    file_name = input('Nhập tên tệp dữ liệu: ')
    data = read_file(file_name)
    # Kiểm tra dữ liệu đọc thành công
    if data:
        # Dữ liệu hợp lệ được lấy bằng chương trình validate_data(data) đã viết ở trên
        valid_data = validate_data(data)
        # Vòng lặp While được sử dụng để yêu cầu nhập đúng đáp án của 25 câu hỏi, vòng lặp kết thúc nếu nhập đúng
        while True:
            answer_key = input('Nhập đáp án của 25 câu hỏi (các giá trị cách nhau dấu phẩy): ')
            # Kiểm tra đáp án có 25 ký tự và chỉ chứa các chữ cái A, B, C, D.
            if len(answer_key.split(',')) == 25 and all(char in 'ABCD' for char in answer_key.replace(',', '')):
                print('Đáp án hợp lệ')
                break
            else:
                print('Đáp án không hợp lệ. Đáp án phải gồm 25 ký tự từ A đến D. Vui lòng nhập lại.')
        # Sau khi nhập đáp án, thực hiện chấm điểm sử dụng chương trình grade_exams(valid_data, answer_key) đã viết ở trên
        scores = grade_exams(valid_data, answer_key)
        # Sau khi chấm điểm xong, thực hiện thống kê điểm sử dụng chương trình calculate_statistics(scores) đã viết ở trên
        calculate_statistics(scores)
        # Ghi dữ liệu điểm số của mỗi sinh viên vào File lưu kết quả
        save_results_file(file_name,valid_data, scores)
        

if __name__ == '__main__':
    main()