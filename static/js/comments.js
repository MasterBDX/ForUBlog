$(function(){
   // ===========  Styels Section ====================
    
    const displayNone = {display:'none'}
    const displayBlock = {display:'block'}
    const disabled = {pointerEvents: 'none',
                      opacity: 0.5,
                     }
   const abled = {pointerEvents: 'auto',
                  opacity: 1
                  }


   // ================ Loading Icon ==================
   const loadingDiv = `
                  <div class="comments-loading">
                    <div>
                        <br />
                           <i class="fas fa-spinner fa-2x fa-pulse"></i>
                        <br />
                     </div>
                  </div>
               `
   
   // ================ Error Message Container ===========
   let errorMessage = ` 
      <div class="alert alert-danger alert-dismissible fade show" role="alert"
                  width: 80%;
                  "
         >
         <p style="font-weight: 500 !important;" 
               class="text-center">
         </p>
            
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
         <span aria-hidden="true">&times;</span>
      </button>
      </div>
      `
      
   // ================                 ==================
   function getErrorMessage(container,message){
      container.html(errorMessage)
      container.find('p').text(message)
      container.css(displayBlock)
   }

   // ================ get Delete Form ===================
   function getDeleteForm(type, btn){
      const id = btn.attr('id')
      const action = btn.attr('delete-url')
      const container = $(`#${type}-${id}`)
      
      const deleteComment = `
         <div class="text-center">
            <p style="
                     display:inline-block;
                     padding:17px;
                     padding-bottom: 0px;
                     color:#e81d1d;
                  ">
               Are you sure ?
               &nbsp;
               <form id="delete-comment-form"
                     comment-id = ${id} 
                     method='post' action="${action}"
                     type="${type}">
                  <button style="" type='submit'    
                     class="btn btn-link">
                     Delete
                  </button>
                  <button type="button" dropdwon-btn="${type}-delete-${id}" id="cancel-btn" class="btn btn-link">
                     Cancel
                  </button>
               </form>
            </p> 
         </div>
      `
      btn.css(disabled)
      let containerChild = container.find(`.deletion-con-${type}-${id}`)    
      containerChild.append(deleteComment).slideDown(1000);
      return true
}
   // ================ get one Comment  ==================

   function getComment(data,type){
      
      let name = 'comment'
      if(type){
         name = type
      }
      let repliesStuff = ''
      
      // ===========   Add Reply Form ====================
      
      if (!data.hasOwnProperty('parent')){
         const replyAddForm = `

            <div style="display:none;" id ="reply-error-message-${data.id}">     
            </div>
                  <form 
                     method="post" 
                     id="replyAddForm"
                     comment-id="${data.id}"
                     action="${data.add_reply_url}" 
                     class="commenting-form">
                     <div class="row">
                        <div class="form-group col-md-12">
                           <label for="usercomment">Content:</label>
                           <textarea style="width: 80%;" 
                                    name="content" cols="40" rows="4" 
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
      
         let replies = data.replies.map((obj)=>{
               return getComment(obj,'reply')
            }).join(' ')
         const repliesCount = data.replies.length
         repliesStuff = `
                  <div class="col-md-12">
                     <button id="add-reply-btn" 
                           class="btn btn-link"
                           comment-id=${data.id}
                           >
                           <i class="fas fa-plus fa-md"></i> 
                           
                           Reply
                     </button>
                     <button id="replies-list-btn"
                             replies-url="${repliesCount}" 
                             comment-id="${data.id}"
                             class="btn btn-link">
                        Replies (<span id="replies-count-${data.id}">${repliesCount}</span>)
                     </button>
                  </div>
               
               <div style="display:none" 
                  id="reply-form-container-${data.id}" 
                  class="col-md-12">
                  <br />
               
                  ${replyAddForm}
               </div>
               <div style="display:none;padding: 33px 60px 0px 24px;" 
                  id="replies-container-${data.id}" 
                  class="col-md-12">
                 ${replies}      
               </div>
               `   
      }
      let dropdownMenu = ''

      if (data.owner){ 
         dropdownMenu = `
                     <div class="btn-group">     
                        <button type="button" class="btn btn-link btn-sm  dropdown-toggle-split" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        <span class="sr-only">Toggle Dropdown</span>
                        <i class="fas fa-ellipsis-v fa-lg"></i>
                     </button>
                     <div class="dropdown-menu"
                           style="
                           width: auto !important;
                           "
                     >
                        <a  class="dropdown-item ${name}-edit ${name}-edit-${data.id}" id="${data.id}"  href="#">Edit</a>
                        <a class="dropdown-item ${name}-delete ${name}-delete-${data.id}" 
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
         ${dropdownMenu}
         </div>

         <div class="comment-body">
         <div class="row">
            <div class="col-sm-10">
               <p edit-url="${data.edit_url}" 
                  id="${name}-content-${data.id}"
                  style="display: inline-block;
                         align-content: ;
                         width: 80%;
                  "
                  >
                  ${data.content}
                  
               </p>
               
              
            </div>
            <div style="display:none; margin: auto;" class='deletion-con-${name}-${data.id}'>
            </div>
            ${repliesStuff}
          
         </div>
         </div>
         
      </div>
      `
      return comment
   }

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
                  $('#load-more-comments-btn').css(displayNone)
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
            getErrorMessage($('#comment-error-message'),error.responseJSON)
         }
      })
   })
   
   // === Click on Edit dropdown btn to show edit form  ==
   
   $(document.body).on('click','.comment-edit',function(e){
      e.preventDefault();
      $(this).css(disabled)
      const commentId = $(this).attr('id')
      
      const commentContentSelector = $('#comment-content-' + commentId);   
      
      const commentContent = commentContentSelector.text().split(' ').filter((letter)=>{
         return letter !== '' && letter !== '\n'
      }).join(' ')
      
      const editUrl = commentContentSelector.attr('edit-url')
      
      const commentForm = `
               <form 
                     method="post"
                     type="comment"
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
 
  // ===== Submit Comment Edit Form to edit comment ========

   $(document.body).on('submit', '#commentsEditForm', function(e){
         e.preventDefault();
         const commentId = $(this).attr('comment-id')
         const endpoint = $(this).attr('action')
         const type = $(this).attr('type')
         const formData = new FormData(event.target);
         const commentContent = formData.get('content')
         $.ajax({
            url:endpoint,
            method:'PATCH',
            data:{'content':commentContent},
            success:(data)=>{                
              $(this).parent().html(commentContent)
              $(`.${type}-edit-${commentId}`).css(abled)
            },
            error:(error)=>{
               console.log(error.status)
            }
         })
   })
   

   // =========== Click on delete dropdown btn to show msg ====================

   $(document.body).on('click','.comment-delete',function(e){
      e.preventDefault();
      getDeleteForm('comment',$(this))      
   })
    
   // ========== Submit Delete Form to delete the comment ==========

   $(document.body).on('submit','#delete-comment-form',function(e){
      e.preventDefault();
      const commentId = $(this).attr('comment-id')
      const endpoint = $(this).attr('action')
      const type = $(this).attr('type')
      $(`.delete-${commentId}`).css({display:'inline'})
      $.ajax({
         url:endpoint,
         method:'DELETE',
         success:(data)=>{
            const comment = $(`#${type}-${commentId}` )
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
         
         $(this).parent().parent().parent().hide()
         $(this).parent().parent().remove()
         const dropdownBtn = $(this).attr('dropdwon-btn')
         console.log(dropdownBtn)
         $(`.${dropdownBtn}`).css(abled);
         
      })

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
         $(`#reply-form-container-${commentId}`).slideToggle('slow');
   })
    
 
   // ================== Replies List Btn ==================
   
   $(document.body).on('click','#replies-list-btn',function(e){
      e.preventDefault();
      const commentId = $(this).attr('comment-id');
      const repliesUrl = $(this).attr('replies-url');
      let repliesContainerParent = $(`#replies-container-${commentId}`)
      repliesContainerParent.toggle('slow')

   })

   // ================== Submit to add new reply ===========

   $(document.body).on('submit','#replyAddForm',function(e){
      e.preventDefault();
      const commentId = $(this).attr('comment-id')
      $(`#replies-container-${commentId}`).prepend(loadingDiv)

      const endpoint = $(this).attr('action')
      const formData = new FormData(event.target);
      const replyContent = formData.get('content')
      $.ajax({
         url:endpoint,
         data:{'content':replyContent},
         method:'post',
         success:(data)=>{
            
            setTimeout(()=>{
               $(`#replies-container-${commentId}`).find('.comments-loading').remove()
               $(`#replies-container-${commentId}`).prepend(getComment(data,'reply'))
               $(this).trigger("reset");
               let repliesCount = $(`#replies-count-${commentId}`)
               repliesCount.text(Number(repliesCount.text()) + 1)
            },1000)
         },
         error:(error)=>{
            if (error.status === 400){
               $(`#replies-container-${commentId}`).find('.comments-loading').remove()
               let errorMessageContainer = $(`#reply-error-message-${commentId}`)
               getErrorMessage(errorMessageContainer,error.responseJSON)
            }

         }
      })


   })
   
   // ============== After click on reply dropdown edit btn ==================
   
      $(document.body).on('click','.reply-edit',function(e){
         e.preventDefault();
         $(this).css(disabled)
         const replyId = $(this).attr('id')
         const replyContentSelector = $('#reply-content-' + replyId);   
         const replyContent = replyContentSelector.text().split(' ').filter((letter)=>{
            return letter !== '' && letter !== '\n'
         }).join(' ')
         
         const editUrl = replyContentSelector.attr('edit-url')
         const replyForm = `
                  <form 
                        method="post"
                        
                        type="reply"
                        comment-id="${replyId}" 
                        id="commentsEditForm" 
                        action="${editUrl}"
                        class="commenting-form">
                        <div class="row">
                           <div class="form-group col-md-12">
                              <label for="usercomment">Content:</label>
                              <textarea required=True name="content" cols="40" rows="4" 
                                    id="usercomment" placeholder="Type your comment" 
                                    class="form-control">${replyContent}</textarea>
                           </div>     
                           <div class="form-group col-md-12">
                              <button  class="my-button" 
                                       type="submit"         
                                       comment-id="${replyId}" 
                                       id="commentEdit-btn-id"
                                       >
                                       Edit
                              </button>
                           </div>
                     </div>
               </form>

         `

      replyContentSelector.html(loadingDiv)
         setTimeout(()=>{   
            replyContentSelector.html(replyForm)
         },
      1000)
      })
   
   // ============== Click on delete dropdown btn ===============
  
    $(document.body).on('click','.reply-delete',function(e){
         e.preventDefault();
         getDeleteForm('reply',$(this))         
 
      })
})