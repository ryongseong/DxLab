<script>
    import { link } from "svelte-spa-router";
    import Image3 from "/public/image3.png?enhanced";
    import Image4 from "/public/image4.png?enhanced";
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
            <img class="head" src={Image4} alt="" />
            <span><strong>GPT</strong>로 작성하기</span>
        </div>
        <div class="card">
            <a use:link href="/self">
                <button class="button">작성하기</button>
            </a>
        </div>
    </div>
    <div class="card-box-b">
        <div class="card-title">
            <img class="head" src={Image4} alt="" />
            <span><strong>Gemini</strong>로 작성하기</span>
        </div>
        <div class="card">
            <a use:link href="/self-gen">
                <button class="button">작성하기</button>
            </a>
        </div>
    </div>
</div>