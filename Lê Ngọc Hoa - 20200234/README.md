# 1. Đặt vấn đề

Trong thời đại công nghệ thông tin phát triển mạnh mẽ hiện nay, việc sử dụng các dịch vụ đám mây (cloud services) đang trở thành một xu hướng không thể phủ nhận. Tuy nhiên, để có thể đưa ra quyết định hợp lý về việc lựa chọn nhà cung cấp dịch vụ đám mây (cloud provider) phù hợp, người dùng cần có đầy đủ thông tin về các dịch vụ và nhà cung cấp đó. Việc thủ công thu thập, so sánh và lựa chọn từ Internet sẽ làm lãng phí nhiều thời gian, công sức và tài nguyên của người dùng, công ty, doanh nghiệp.

Để giải quyết vấn đề này, xây dựng một công cụ thu thập dữ liệu về các cloud services / cloud provider sẽ là một giải pháp hữu hiệu. Công cụ này sẽ giúp người dùng thu thập và tổng hợp thông tin về các tính năng, đặc điểm của các dịch vụ đám mây và các nhà cung cấp, từ đó giúp họ đưa ra quyết định hợp lý về việc lựa chọn nhà cung cấp dịch vụ phù hợp với nhu cầu sử dụng của mình. Trong phạm vi project I, em phụ trách tìm hiểu và phần công việc lập trình công cụ thu thập dữ liệu từ các nhà cung cấp dịch vụ. Với đầu ra (output) là danh sách các trường dữ liệu thu thập được tối đa từ các nhà cung cấp. (RAM, CPU, price, security options, …). Phần dữ liệu đầu ra này sẽ trở thành dữ liệu đầu vào cho bạn Trịnh Phú Quang làm cơ sở để đánh giá các dịch vụ của nhà cung cấp, từ đó đưa ra lựa chọn phù hợp với từng nhu cầu cho người dùng. Trong quá trình thực hiện em đã gặp một số thách thức, khó khăn cần vượt qua.

Thách thức đầu tiên em cần giải quyết là các thông tin được nhà cung cấp công khai cho khách hàng không thống nhất theo một định dạng, mỗi nhà cung cấp dịch vụ có giao diện sản phẩm khác nhau, cách thức giới thiệu, thu hút người dùng lựa chọn sản phẩm của mình cũng khác nhau, chẳng hạn nhà cung cấp A đưa ra giới thiệu sản phẩm ở dạng bảng, trong khi nhà cung cấp B trình bày giao diện theo dạng khối (block), một số nhà cung cấp có sự biến đổi về số liệu tùy thuộc vào người dùng được phép thay đổi thông tin các trường RAM , CPU, thời gian sử dụng, …

Một khó khăn khác em cần vượt qua là vấn đề phạm vi số lượng thông tin sản phẩm công khai tới người dùng của mỗi nhà cung cấp dịch vụ sẽ khác nhau, các lựa chọn được mỗi nhà cung cấp đưa ra cũng vô cùng đa dạng. Thông thường các nhà cung cấp sẽ chỉ công khai các trường dữ liệu thuộc về thế mạnh có thể hỗ trợ của mình. Trong khi phần dữ liệu đầu ra yêu cầu cần thu thập tối đa các trường dữ liệu của từng nhà cung cấp theo một định dạng chung đã quy ước từ trước. Điều đó dẫn tới một số trường dữ liệu sẽ bị rỗng do không thể thu thập trực tiếp qua trang chủ từ các nhà cung cấp dịch vụ.

Cuối cùng, em cần giải quyết khó khăn về kỹ thuật crawl. Do giao diện của mỗi nhà cung cấp dịch vụ đều khác nhau, phần trình bày các dữ liệu công khai trong dạng HTML cũng khác nhau. Chẳng hạn, nhà cung cấp A trình bày giao diện gồm các dữ liệu thông số về Storage trong thẻ <div> với giá trị thuộc tính class là x, trong khi nhà cung cấp B lựa chọn trình bày giá trị này trong thẻ <p> với giá trị thuộc tính class là y, thêm vào đó là các hiệu ứng thay đổi khi người dùng di chuyển con trỏ chuột tới giá trị này. Hoặc một số nhà cung cấp còn lưu trữ lại các đoạn code là thông tin của một số lựa chọn sản phẩm trong quá khứ (đã dừng cung cấp) nhưng ẩn các dữ liệu này đi, hay đơn giản là biến chúng thành các dòng comment … Những sự bất đồng và các thông tin gây nhiễu này đã tạo ra một thách thức lớn với công cụ crawl được em xây dựng.
# 2. Mục tiêu và phạm vi đề tài

Công cụ xây dựng cuối cùng cần đưa ra danh sách các nhà cung cấp dịch vụ phù hợp với nhu cầu người dùng. Bởi vậy, mục tiêu project I về phần lập trình công cụ thu thập dữ liệu của em cần đưa ra output gồm các trường thông tin có thể thu thập tối đa từ danh sách các nhà cung cấp. Từ đó làm dữ liệu đầu vào cho phần công việc đánh giá khả năng cung cấp, sản phẩm của các nhà cung cấp.

Kết quả công cụ thu thập dữ liệu do em xây dựng đạt hiệu năng tốt. Tuy nhiên còn tồn tại vấn đề một số trường dữ liệu nhận giá trị rỗng. Điều này xảy ra là do các hạn chế về thông tin công khai về sản phẩm từ các nhà cung cấp không đạt tính thống nhất, số lượng trường dữ liệu giới thiệu tới người dùng còn phụ thuộc chủ quan vào chính các nhà cung cấp, cách thức trình bày giao diện sản phẩm bất đồng. Đây đều là các khó khăn và mục tiêu mà em cần giải quyết trong phạm vi Project I. Sau khi khắc phục các hạn chế trên, em đã hướng tới phát triển công cụ thu thập có hiệu năng tối ưu hơn, tiết kiệm tài nguyên đồng thời thêm chức năng kiểm tra tính cập nhật của nhà cung cấp trên giao diện giới thiệu sản phẩm của họ.
# 3. Định hướng giải pháp

Để thực hiện ý tưởng xây dựng công cụ thu thập dữ liệu về các cloud services /  cloud provider, em đã có định hướng giải pháp trong việc vượt qua, khắc phục các khó khăn nêu trên như sau:

-	Xác định danh sách các nhà cung cấp: tìm kiếm thủ công qua Internet gồm các trang web thống kê các nhà cung cấp dịch vụ, các diễn đàn công nghệ, … 
-	Xây dựng các chương trình thu thập dữ liệu: Cần phát triển các chương trình để tự động thu thập thông tin từ các nguồn dữ liệu đã xác định. Chương trình sử dụng kết hợp các thư viện, module gồm Selenium, BeautifulSoup, requests. 
-	Đầu vào dữ liệu (input) bao gồm thành phần input dùng cho crawl và input cho kiểm tra cập nhật (update). Thành phần input dùng cho crawl sử dụng định dạng cấu trúc JSON. Thành phần input dùng cho kiểm tra cập nhật tương ứng mỗi nhà cung cấp là một dòng dưới dạng A:B. Trong chương trình em lựa chọn thư viện json.
-	Xử lý dữ liệu: Cần xử lý dữ liệu thu thập được từ các nguồn dữ liệu để có thể sử dụng và truy xuất được dễ dàng. Xử lý dữ liệu bằng các hàm trích xuất thông tin do em tự xây dựng kết hợp các định dạng từ kỹ thuật REGEX. Trong đó em có sử dụng thư viện re.
-	Lưu trữ dữ liệu: Lưu trữ dữ liệu trong các tệp định dạng .CSV, bao gồm các cột, tên mỗi cột tương ứng là tên các trường dữ liệu thu thập, giá trị mỗi cột là giá trị thu thập được của các nhà cung cấp. Đồng thời lưu trữ các hash của source code trang chủ các nhà cung cấp trong một tệp văn bản, mỗi dòng tương ứng với một nhà cung cấp. Trong chương trình em lựa chọn thư viện pandas.
-	Kiểm tra và cập nhật thông tin: Cần kiểm tra và cập nhật thường xuyên thông tin về các dịch vụ đám mây và các nhà cung cấp để đảm bảo tính chính xác và đầy đủ của thông tin thu thập được. Sử dụng so sánh hash để xử lý việc kiểm tra tình trạng cập nhật của các nhà cung cấp. Công nghệ hash được em lựa chọn là MD5, thư viện em sử dụng là hashlib.
-	Dữ liệu đầu ra (output) cho chương trình bao gồm các tệp định dạng .CSV tương ứng với mỗi loại nhà cung cấp, trong đó gồm danh sách tên các trường dữ liệu thu thập, mỗi cột gồm giá trị thu thập được từ từng lựa chọn sản phẩm của mỗi nhà cung cấp.

# 4. Hướng dẫn sử dụng

Khởi chạy chương trình:

```
python3 crawl.py
```
