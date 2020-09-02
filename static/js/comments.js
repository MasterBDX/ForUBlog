$(function(){


   // ================ Loading Icon ==================
   const loadingDiv = `
                  <div class="comments-loading">
                     <i class="fas fa-spinner fa-2x fa-pulse"></i>
                  </div>
               `
   
   // ================ get one Comment  ==================

   function getComment(data){
      const name = 'comment'
   
         // ===========   Add Reply Form ====================

         const replyAddForm = `
               
                  <form 
                     method="post" id="replyAddForm"
                     action="${data.add_reply_url}" 
                     class="commenting-form">
                     <div class="row">
                        <div class="form-group col-md-12">
                           <label for="usercomment">Content:</label>
                           <textarea name="content" cols="40" rows="4" 
                                    id="usercomment" placeholder="Type your reply" 
                                    class="form-control"></textarea>
                        </div>     
                           <div class="form-group col-md-12">
                              <button  class="my-button" type="submit" >
                                    Add
                              </button>
                           </div>
                     </div>
            </form> `

      let repliesStuff = ''
      if (!data.hasOwnProperty('parent')){
         repliesStuff = `
                  <div class="col-md-12">
                     <button id="add-reply-btn" 
                           class="btn btn-link"
                           comment-id=${data.id}
                           >
                        Add Reply
                     </button>
                     <button id="replies-list-btn"
                             replies-url="${data.replies_url}" 
                             class="btn btn-link">
                        replies (0)
                     </button>
                  </div>
               
               <div style="display:none" 
                  id="reply-form-container-${data.id}" 
                  class="col-md-12">
                  <br />
               
                  ${replyAddForm}
               </div>
               <div style="display:none" 
                  id="replies-container-${data.id}" 
                  class="col-md-12">
                 <div class="replies">

                 </div>
                 <div class="text-center">
                     <hr />
                  <button id='load-more-comments-btn' class="btn btn-link">
                     Load more
                  </button>
               </div>
               
               
               </div>

                     `   
      }
      let dropdownMenu = ''

      if (data.owner){
         
         dropdownMenu = `
                     <div class="btn-group">     
                     <button type="button" class="btn btn-sm btn-danger dropdown-toggle dropdown-toggle-split" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                     <span class="sr-only">Toggle Dropdown</span>
                     </button>
                     <div class="dropdown-menu">
                        <a class="dropdown-item ${name}-edit edit-${data.id}" id="${data.id}"  href="#">Edit</a>
                        <a class="dropdown-item ${name}-delete delete-${data.id}" 
                           delete-url="${data.delete_url}"
                           id="${data.id}" href="#">Delete</a>
               
               
                     </div>
                  </div>
         ` 
      }
      const comment = `
         <div class="comment" id="${name}-${data.id}">
         
         <div class="comment-header d-flex justify-content-between">
         <div class="user d-flex align-items-center">
            <div class="image">
               <img src="${data.image_url}" alt="..." class="img-fluid rounded-circle"></div>
            <div class="title">
               <strong>${data.username}</strong>
               <span class="date">${data.timesince} ago</span>
            </div>
         </div>
         </div>

         <div class="comment-body">
         <div class="row">
            <div class="col-sm-10">
               <p edit-url="${data.edit_url}" 
                  id="${name}-content-${data.id}"
                  style="display: inline-block;
                         align-content: ;
                         width: 90%;
                  "
                  >
                  ${data.content}
                  
               </p>
               ${dropdownMenu}
              
            </div>
            ${repliesStuff}
          
         </div>
         </div>
      </div>
      `
      return comment
   }

   // =================================================


   // ==============  Global Vars & funcs ====================
   let nextUrl;
   let commentsContainer = $('#comments-container-id');
   let commentsCount = $("#comments-count");
   const commentsFetcheUrl = commentsContainer.attr('comments-list-url')

   function checkNum (strNum){
      return Number(strNum)
   }


   // ================ get Comments List  ==================

   function getCommentsList(appended){
      let url = nextUrl ; 
      if (!nextUrl){
         url = commentsFetcheUrl
      } 
         $.ajax({
            url:url,
            success:(data) =>{              
               if (data.next){
                  nextUrl = data.next;
               }else{
                  $('#load-more-comments-btn').css({'display':'none'})
               }
               let commentsArr = data.results.map((obj)=>{
                     return getComment(obj)
                  })
                  if (appended){
                     commentsContainer.append(commentsArr.join(' '))    
                  }else{
                    commentsContainer.html(commentsArr.join(' '))
                  }
               }
               ,error:(error) =>{
               console.log(error.status)
            }
         })
         
   }
   
   // ========= Submit Comment Form To add comment =====
   
   $('#commentsForm').on('submit',function(event){
      event.preventDefault();
      const endpoint = $(this).attr('action')
      const formData = new FormData(event.target);
      $.ajax({
         url:endpoint,
         method:'POST',
         data:{'content':formData.get('content')},
         success:(data)=>{
            
            commentsContainer.prepend(loadingDiv)
            setTimeout(()=>{
               $('#comments-container-id .comments-loading').remove()
               commentsContainer.prepend(getComment(data))
               const Num = checkNum(commentsCount.text()) 
               commentsCount.text(Num + 1)
               $(this).trigger("reset"); 
            }
               ,2000)
            
            
            
            
         },
         error:(error)=>{
            console.log(error.status)
         }
      })
   })

   // ===================================================
   
   // === Click on Edit dropdown btn to show edit form  ==
   
   $(document.body).on('click','.comment-edit',function(e){
      e.preventDefault();
      $(this).css({'display':'none'})
      const commentId = $(this).attr('id')
      
      const commentContentSelector = $('#comment-content-' + commentId);   
      
      const commentContent = commentContentSelector.text().split(' ').filter((letter)=>{
         return letter !== '' && letter !== '\n'
      }).join(' ')
      console.log(commentContent)
      const editUrl = commentContentSelector.attr('edit-url')
      
      const commentForm = `
               <form 
                     method="post"
                     comment-id="${commentId}" 
                     id="commentsEditForm" 
                     action="${editUrl}"
                     class="commenting-form">
                     <div class="row">
                        <div class="form-group col-md-12">
                           <label for="usercomment">Content:</label>
                           <textarea required=True name="content" cols="40" rows="4" 
                                  id="usercomment" placeholder="Type your comment" 
                                  class="form-control">${commentContent}</textarea>
                        </div>     
                        <div class="form-group col-md-12">
                           <button  class="my-button" 
                                    type="submit"         
                                    comment-id="${commentId}" 
                                    id="commentEdit-btn-id"
                                    >
                                    Edit
                           </button>
                        </div>
                  </div>
             </form>

      `

     commentContentSelector.html(loadingDiv)
     setTimeout(()=>{
         
         commentContentSelector.html(commentForm)
      
      },
     1000)
      
   })

   // ======================================================
   
  // ===== Submit Comment Edit Form to edit comment ========

   $(document.body).on('submit', '#commentsEditForm', function(e){
         e.preventDefault();
         const commentId = $(this).attr('comment-id')
         const endpoint = $(this).attr('action')
         const formData = new FormData(event.target);
         const commentContent = formData.get('content')
         $.ajax({
            url:endpoint,
            method:'PATCH',
            data:{'content':commentContent},
            success:(data)=>{                
              $(this).parent().html(commentContent)
              $(`.edit-${commentId}`).css({'display':'inline'})
            },
            error:(error)=>{
               console.log(error.status)
            }
         })
   })
   
   // ======================================================

   // =========== Click on delete dropdown btn to show msg ====================

   $(document.body).on('click','.comment-delete',function(e){
      e.preventDefault();
      
      const commentId = $(this).attr('id')
      const action = $(this).attr('delete-url')
      const comment = $('#comment-' + commentId)
      const deleteComment = `
         <div class="text-center">
            <p style="
                     display:inline-block;
                     border:1px solid #555;
                     border-radius:10px;
                     padding:17px;
                     margin-bottom:20px;
                  ">
               Are you sure you want to delete this comment ?
               &nbsp;
               <form id="delete-comment-form"
                     comment-id = ${commentId} 
                     method='post' action="${action}">
                  <button style="" type='submit'    
                     class="btn btn-danger">
                     Delete
                  </button>
                  <button type="button" id="cancel-btn" class="btn btn-link">
                     Cancel
                  </button>
               </form>
             
            </p> 
         </div>
      `
      $(this).css({display:'none'})
      comment.append(deleteComment);
   })
   // ==============================================================
   
   // ========== Submit Delete Form to delete the comment ==========

   $(document.body).on('submit','#delete-comment-form',function(e){
      e.preventDefault();
      const commentId = $(this).attr('comment-id')
      const endpoint = $(this).attr('action')
      // $(`.delete-${commentId}`).css({display:'inline'})
      $.ajax({
         url:endpoint,
         method:'DELETE',
         success:(data)=>{
            const comment = $('#comment-' + commentId)
            comment.html(loadingDiv)
            setTimeout(()=>{
               comment.remove()
               const Num = checkNum(commentsCount.text()) 
               commentsCount.text(Num - 1) 
            },1000)
            
      
         },
         error:()=>{

         }
      })

   })
   // =============== Remove Delete Msg ===================
      $(document.body).on('click','#cancel-btn',function(e){
         e.preventDefault();
         
         $(this).parent().parent().parent().remove()
      })

   // =====================================================
   //  ============= Commetns Load More Btn ================
      $('#load-more-comments-btn').on('click',function(e){
            e.preventDefault();
            $(this).html(loadingDiv);
            setTimeout(()=>{
               commentsContainer.append(getCommentsList(true))
               $(this).text('Load more');
            },1000)

         })

   // ======================================================
   getCommentsList()



   // ================== Replies Section ===================
   
   //====== Add Reply btn to show add reply form =======

   $(document.body).on('click','#add-reply-btn',function(){
         const commentId = $(this).attr('comment-id')
         $(`#reply-form-container-${commentId}`).slideToggle();
   })
   // ======================================================


   // ================== Get Replies List ==================
   
   // let nextRepliesUrl;
   // function getCommentsList(appended){
   //    let url = nextRepliesUrl ; 
   //    if (!nextUrl){
   //       url = commentsFetcheUrl
   //    } 
   //       $.ajax({
   //          url:url,
   //          success:(data) =>{              
   //             if (data.next){
   //                nextUrl = data.next;
   //             }else{
   //                $('#load-more-comments-btn').css({'display':'none'})
   //             }
   //             let commentsArr = data.results.map((obj)=>{
   //                   return getComment(obj)
   //                })
   //                if (appended){
   //                   commentsContainer.append(commentsArr.join(' '))    
   //                }else{
   //                  commentsContainer.html(commentsArr.join(' '))
   //                }
   //             }
   //             ,error:(error) =>{
   //             console.log(error.status)
   //          }
   //       })
         
   // }
   
   // ======================================================
   // ================== Replies List Btn ==================
   $(document.body).on('click','#replies-list-btn',function(e){
      e.preventDefault();
      const repliesUrl = $(this).attr('replies-url');
      console.log(repliesUrl)
   })
   // ======================================================
   // ================== Submit to add new reply ===========
   $(document.body).on('submit','#replyAddForm',function(e){
      e.preventDefault();
      const endpoint = $(this).attr('action')
      const formData = new FormData(event.target);
      console.log(event.target)
      const replyContent = formData.get('content')
      $.ajax({
         url:endpoint,
         data:{'content':replyContent},
         method:'post',
         success:(data)=>{
            console.log(data)
            $(this).trigger("reset"); 
         },
         error:(error)=>{
            console.log(error.status)
         }
      })


   })

   // ======================================================
})