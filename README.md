# aif-service-guide-gradio
aif 서비스 사용량 검사방법


software version
python3, gradio version 3.1.5

설명

순서
1. URL를 통해 gradio web server에 사용자 키값 전달 방법
   - URL Parameter 로 키값 전달 : 예시) http(s)://서비스주소/?key=value
3. gradio 에 전달된 사용자 키값을 변수로 가져오는 방법
   - gradio _js=get_window_url_params 사용하여 url_params 을  key : value 형태로 가져옴
   default.py 참고 
5. 사용자 키값을 인공지능팩토리 API 서버에 전달하여 사용량 검사를 실행하는 방법
   - predict 함수 실행할 때 url_params['key']  를 가져와서 sendRequestForService 함수로 전달
   - sendRequestForService 함수는 API 서버에 검사요청한 후 결과를 리턴함
   - 리턴된 json 형태의 결과에서 json_data['ct'] == 1 이면 사용자는 오류를 표시해야 함
   - 오류는 gradio Label interface를 통해 보여줌
    - 오류가 없는 경우 정상적인 결과를  리턴하면 됨

   - API 서버 오류 종류는 아래와 같다
   {ct : 1, message: "사용기간이 만료되었습니다."}
   {ct : 1, message: "사용횟수를 초과했습니다."}
7. chatbot으로 수행할때 유의 할 점
   - 실행시 gen_btn 버튼으로 초기화
   - gen_btn 의 _js=get_window_url_params 사용하여 url_params 을  key : value 형태로 가져옴
   - chat 함수 실행할 때 url_params['key']  를 가져와서 sendRequestForService 함수로 전달 이후과정은 위와 동일 
   default_chatbot.py 참고 
