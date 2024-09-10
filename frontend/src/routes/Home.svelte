<script>
  import { link } from "svelte-spa-router";
  import Image2 from "/public/image2.png?enhanced";
  import Image3 from "/public/image3.png?enhanced";
  import Image4 from "/public/image4.png?enhanced";
  import Image5 from "/public/image5.png?enhanced";
</script>

<style>  
  .container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 40px;
    margin-top: 50px;
    gap: 40px;
  }

  .card {
    width: 451px;
    height: 590px;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    background-color: white;
    text-align: center;
    box-shadow: 5px 5px 4px 0px #00000040;
  }

  .card-title {
    color: #8a56d8;
    margin-bottom: 10px;
    font-family: Inter;
    font-size: 32px;
    line-height: 38.73px;
    width: 459px;
    height: 101px;
    top: 194px;
    left: 838px;
    gap: 0px;
    opacity: 0px;
  }

  .card-header {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 10px;
    background-color: #FFFFFF;
    border-bottom: #FFFFFF;
  }

  img {
    width: 170px;
    height: 170px;
    top: 291px;
    left: 217px;
    gap: 0px;
    border-radius: 20px 0px 0px 0px;
    opacity: 0px;
  }

  img.head {
    width: 84px;
    height: 84px;
    top: 194px;
    left: 838px;
    gap: 0px;
    opacity: 0px;
  }

  .card-subtitle {
    color: #9470F7;
    width: 274px;
    height: 98px;
    top: 356px;
    left: 380px;
    gap: 0px;
    border: 1.5px 0px 0px 0px;
    opacity: 0px;
    font-family: Inter;
    font-size: 20px;
    font-weight: bold;
    line-height: 24.2px;
    text-align: left;
  }

  .card-text {
    width: 274px;
    height: 48px;
    top: 332px;
    left: 380px;
    gap: 0px;
    opacity: 0px;
    font-family: Inter;
    font-size: 20px;
    font-weight: 400;
    line-height: 24.2px;
    text-align: left;
    color: #000000;
  }

  .card-text-a {
    margin-top: 40px;
    margin-bottom: 40px;
    color: #444;
    font-size: 24px;
    line-height: 1.5;
  }

  .button {
    margin-top: 10px;
    font-size: 40px;
    color: white;
    background-color: #9470F7B0;
    text-align: center;
    border: none;
    border-radius: 30px;
    cursor: pointer;
    width: 321px;
    height: 69px;
    transition: background-color 0.3s;
  }

  .card-box-a {
    width: 489px;
    height: 691px;
    margin-left: 50px;
    top: 187px;
    gap: 0px;
    opacity: 0px;
    position: flex;
  }

  .card-box-b {
    width: 489px;
    height: 691px;
    margin-left: 50px;
    top: 187px;
    gap: 0px;
    opacity: 0px;
    position: flex;
  }

  .button:hover {
    background-color: #a07bfa;
  }
</style>

<div class="container">
  <div class="card-box-a">
    <div class="card-title">
      <img class="head" src={Image5} alt=""/>
      <span style="text-align: center;">자격증 <strong>문제 풀기</strong></span>
    </div>
    <div class="card">
      <div class="card-header">
        <img src={Image2} alt="" />
        <div class="card-text">
          원하는 직군의 자격증의 문제를 풀어보고 싶어!! <br><br>
          <span class="card-subtitle">자기 개발을 원하는 사용자</span>
        </div>
      </div>
      <div class="card-text-a">
          <strong style="color: #9470F7;">생성형 AI</strong>를 이용한 다양한 문제 생성!! <br><br>
          <strong style="color: #9470F7;">AI</strong>가 해주는 자동 채점으로 결과 확인!! <br><br>
          자격증 문제에 특화 되어있는 <strong style="color: #9470F7;">AI시스템</strong>!!
      </div>
      <a use:link href="/exam">
        <button class="button">문제풀기</button>
      </a>
    </div>
  </div>
  <div class="card-box-b">
    <div class="card-title">
      <img class="head" src={Image4} alt="" />
      <span><strong>자기소개서</strong> 작성하기</span>
    </div>
    <div class="card">
      <div class="card-header">
        <img src={Image3} alt="" />
        <div class="card-text">
          원하는 직군의 자기소개서를 작성하고 싶어!! <br><br>
          <span class="card-subtitle">취업을 원하는 사용자</span>
        </div>
      </div>
      <div class="card-text-a">
          <strong style="color: #9470F7;">생성형 AI</strong>를 이용한 다양한 자소서 생성!! <br><br>
          <strong style="color: #9470F7;">AI</strong>가 주는 키워드로 내용 손실 최소화!! <br><br>
          자기소개서에 특화 되어있는 <strong style="color: #9470F7;">AI시스템</strong>!!
      </div>
      <a use:link href="/select">
        <button class="button">작성하기</button>
      </a>
    </div>
  </div>
</div>
