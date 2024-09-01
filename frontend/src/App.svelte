<script>
  import Router from 'svelte-spa-router'
  import GPT from "./routes/GPT.svelte"
  import UserCreate from './routes/UserCreate.svelte';
  import UserLogin from './routes/UserLogin.svelte';
  import Navigation from './components/Header.svelte';
  import QuestionModify from './routes/QuestionModify.svelte';
  import Home from './routes/Home.svelte';
  import Exam from './routes/Exam.svelte';
  import ExamDetail from './routes/Exam_detail.svelte';
  import { wrap } from 'svelte-spa-router/wrap'; 

  const routes = {
    '/': Home,
    '/self': GPT,
    '/exam': Exam,
    '/exam-detail': ExamDetail,
    '/user-create': UserCreate,
    '/user-login': UserLogin,
    '/question-modify/:question_id': QuestionModify,
  }
</script>

<Navigation />
<Router {routes}/>