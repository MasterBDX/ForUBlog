$(function(){

   $('#commentsForm').on('submit',function(event){
      event.preventDefault();
      const endpoint = $(this).attr('action')
      console.log(endpoint)
      $.ajax({
         url:endpoint,
         success:(data)=>{
            console.log(data)
         },
         error:(error)=>{
            console.log(error.status)
         }
      })
   })

   function getComment(data){
      const comment = `
         <div class="comment" id="comment-${data.id}">
         
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
            <div class="col-md-10">
               <p id="comment-content-${data.id}">${data.content}</p>
            </div>
            <div class="col-md-2">
               <div class="btn-group">
            
               <button type="button" class="btn btn-sm btn-danger dropdown-toggle dropdown-toggle-split" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
               <span class="sr-only">Toggle Dropdown</span>
               </button>
               <div class="dropdown-menu">
               <a class="dropdown-item" href="#">Edit</a>
               <a class="dropdown-item" href="#">Delete</a>
              
              
               </div>
            </div>
            </div>
         </div>
         </div>
      </div>
      `
      return comment
   }

   function getCommentsList(){
      const endpoint = $('#comments-container-id').attr('comments-list-url')
      $.ajax({
         url:endpoint,
         success:(data) =>{
            let commentsArr = data.map((obj)=>{
               return getComment(obj)
            })
            $('#comments-container-id').html(commentsArr.join(' '))
         }
         ,error:(error) =>{
            console.log(error.status)
         }
      })    
   }
getCommentsList()
})