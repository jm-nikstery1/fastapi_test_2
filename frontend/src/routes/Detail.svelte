<!-- 질문 상세 화면  + 답변 등록 화면 + 질문 상세 화면에 답변 표시-->

<script>
  import fastapi from "../lib/api"
  import Error from "../components/Error.svelte"
  import {link, push} from 'svelte-spa-router'  //질문 목록 버튼 추가 
  import {is_login, username} from '../lib/store'  //로그인 안하면 작동 안됨
  import moment from 'moment/min/moment-with-locales'
  moment.locale('ko')
  import { marked } from 'marked'   //마크다운 적용

  export let params = {}
  let question_id = params.question_id
  //console.log('question_id:' + question_id) 
  let question = {answers:[], voter:[], content:''}
  let content = ""   // 답변에 대한 내용을 담음

  let error ={detail:[]}

  function get_question() {
    fastapi("get", "/api/question/detail/"+ question_id, {}, (json) =>{
      question = json
    })
  }

  get_question()

  // 답변등록 버튼 누르면 답변 등록 API를 호출하도록 함
  function post_answer(event){
    event.preventDefault()
    let url = "/api/answer/create/" + question_id
    let params ={
      content: content
    }
    fastapi("post", url, params, (json)=>{
      content=""
      error = {detail:[]}
      get_question()
      },
      (err_json)=>{
        error = err_json
      }
    )
  }

  function delete_question(_question_id){    // 질문 삭제 버튼
    if(window.confirm("정말로 삭제하시겠습니까?")){
      let url = '/api/question/delete'
      let params = {
        question_id: _question_id
      }
      fastapi('delete', url, params,
      (json) =>{
        error = err_json
      }
      )      
    }
  }

  function delete_answer(answer_id) {    // 답변 삭제 버튼 
        if(window.confirm('정말로 삭제하시겠습니까?')) {
            let url = "/api/answer/delete"
            let params = {
                answer_id: answer_id
            }
            fastapi('delete', url, params, 
                (json) => {
                    get_question()
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }

    function vote_question(_question_id) {
        if(window.confirm('정말로 추천하시겠습니까?')) {
            let url = "/api/question/vote"
            let params = {
                question_id: _question_id
            }
            fastapi('post', url, params, 
                (json) => {
                    get_question()
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }

    function vote_answer(answer_id) {
        if(window.confirm('정말로 추천하시겠습니까?')) {
            let url = "/api/answer/vote"
            let params = {
                answer_id: answer_id
            }
            fastapi('post', url, params, 
                (json) => {
                    get_question()
                },
                (err_json) => {
                    error = err_json
                }
            )
        }
    }



</script>


<!--  부트스트립 적용전 
<h1>제목</h1>
<h1>{question.subject}</h1>
<div>
  내용
  줄바꿈은 조건이 까다롭구나
</div>
<div>
  {question.content}
</div>
<ul>
  {#each question.answers as answer}
      <li>{answer.content}</li>
  {/each}
</ul>
<Error error ={error}/>
<form method ="post">
  <textarea rows="15" bind:value={content}></textarea>
  <input type="submit" value="답변등록" on:click="{post_answer}">
</form>

화면 예쁘게 꾸미기 
<style>
  textarea{
    width:100%;
  }
  input[type=submit]{
    margin-top:10px;
  }
</style>-->

<div class="container my-3">
  <!-- 질문 -->
  <h2 class="border-bottom py-2">{question.subject}</h2>
  <div class="card my-3">
      <div class="card-body">
          <div class="card-text">{@html marked.parse(question.content)}</div>
          <div class="d-flex justify-content-end">
              {#if question.modify_date }
              <div class="badge bg-light text-dark p-2 text-start mx-3">
                  <div class="mb-2">modified at</div>
                  <div>{moment(question.modify_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
              </div>
              {/if}
              <div class="badge bg-light text-dark p-2 text-start">
                <div class="mb-2">{ question.user ? question.user.username : ""}</div>
                  <div>{moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")} </div>   <!--한국식 시간-->
              </div>
          </div>
          <!--질문 수정 버튼-->
          <div class="my-3">
            <button class="btn btn-sm btn-outline-secondary"
                on:click="{vote_question(question.id)}"> 
                추천
                <span class="badge rounded-pill bg-success">{ question.voter.length }</span>
            </button>
            {#if question.user && $username === question.user.username }
              <a use:link href="/question-modify/{question.id}" 
              class="btn btn-sm btn-outline-secondary">수정</a>
              <button class="btn btn-sm btn-outline-secondary"
              on:click={() => delete_question(question.id)}>삭제</button>
            {/if}
          </div>
      </div>
  </div>

  <button class="btn btn-secondary" on:click ="{() => {
    push('/')
  }}">목록으로</button>

  <!-- 답변 목록 -->
  <h5 class="border-bottom my-3 py-2">{question.answers.length}개의 답변이 있습니다.</h5>
  {#each question.answers as answer}
  <div class="card my-3">
      <div class="card-body">
          <div class="card-text">{@html marked.parse(answer.content)}</div>
          <div class="d-flex justify-content-end">
            {#if answer.modify_date }  <!--답변 상세 화면에 수정일시 표시-->
              <div class="badge bg-light text-dark p-2 text-start mx-3">
                  <div class="mb-2">modified at</div>
                  <div>{moment(question.modify_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>
              </div>
              {/if}
              <div class="badge bg-light text-dark p-2 text-start">
                <div class="mb-2">{ answer.user ? answer.user.username : ""}</div>
                <div>{moment(answer.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</div>                  
              </div>
          </div>
          <div class="my-3">  <!--답변 수정 버튼-->
            <button class="btn btn-sm btn-outline-secondary"
                on:click="{vote_answer(answer.id)}"> 
                추천
                <span class="badge rounded-pill bg-success">{ answer.voter.length }</span>
            </button>
            {#if answer.user && $username === answer.user.username }
            <a use:link href="/answer-modify/{answer.id}" 
                class="btn btn-sm btn-outline-secondary">수정</a>
            <button class="btn btn-sm btn-outline-secondary"
                on:click={() => delete_answer(answer.id) }>삭제</button>
            {/if}
        </div>
      </div>
  </div>
  {/each}
  <!-- 답변 등록 -->
  <Error error={error} />
  <form method="post" class="my-3">
      <div class="mb-3">
          <textarea rows="10" bind:value={content} disabled={$is_login ? "" : "disabled"} class="form-control" />
      </div>
      <input type="submit" value="답변등록" class="btn btn-primary{$is_login ? '': 'disabled'}" on:click="{post_answer}" />  <!--로그인 안하면 버튼 비활성화-->
  </form>
</div>
