<script>
    import { link } from 'svelte-spa-router';
    import { access_token, is_login, username } from '../lib/store';
</script>

<style>  
    .navbar-custom {
        background: linear-gradient(to right, #b69dfa, #d0ddf9);
    }

    .navbar-brand {
        font-weight: 400;
        color: white;
        font-family: 'Inter', sans-serif;
        font-size: 64px;
        margin-left: 60px;
    }

    .navbar-nav.al {
        margin-left: 80px;
    }

    .navbar-nav.ag {
        margin-right: 40px;
    }

    .nav-link {
        color: white;
    }

    .nav-link:hover {
        text-decoration: underline;
    }

    .nav-item {
        font-size: 30px;
        padding: 10px;
    }
    .user-name {
        color: white;
        margin-top: 5px;
    }
</style>

<nav class="navbar navbar-expand-lg navbar-custom">
    <div class="container-fluid">
        <a use:link class="navbar-brand" href="/">DxLab</a>
        <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0 al">
                <li class="nav-item">
                    <a use:link href='/exam' class="nav-link">문제풀기</a>
                </li>
                <div class="nav-item" style="color: white; margin-top:5px;">|</div>
                <li class="nav-item">
                    <a use:link href='/self' class="nav-link">자기소개서 작성</a>
                </li>
            </ul>
            <ul class="navbar-nav ms-auto mb-2 mb-lg-0 ag">
                {#if $is_login}
                    <li class="nav-item">
                        <p class="user-name">{$username}</p>
                    </li>
                    <div class="nav-item" style="color: white; margin-top:5px; margin-left: 5px;">|</div>
                    <li class="nav-item">
                        <a use:link href="/user-login" class="nav-link" on:click={() => {
                            $access_token = '';
                            $username = '';
                            $is_login = false;
                        }}>로그아웃</a>
                    </li>
                {:else}
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/user-login">로그인</a>
                    </li>
                    <div class="nav-item" style="color: white; margin-top:5px;">|</div>
                    <li class="nav-item">
                        <a use:link class="nav-link" href="/user-create">회원가입</a>
                    </li>
                {/if}
            </ul>
        </div>
    </div>
</nav>
