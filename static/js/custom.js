
$(function () {

  /* SCRIPT TO OPEN THE MODAL WITH THE PREVIEW */
  $('.scrollDown').click((e) => {
    e.preventDefault()

    $('html, body').animate({
      scrollTop: $('#about-blog').offset().top
    }, 500
    )
  })
  $('#id_file').change(function () {
    if (this.files && this.files[0]) {
      var reader = new FileReader()
      reader.onload = function (e) {
        $('#image').attr('src', e.target.result)
        $('#modalCrop').modal('show')
      }

      reader.readAsDataURL(this.files[0])
    }
  })

  /* SCRIPTS TO HANDLE THE CROPPER BOX */
  var $image = $('#image')
  var cropBoxData
  var canvasData
  $('#modalCrop').on('shown.bs.modal', function () {
    $image.cropper({
      viewMode: 1,
      aspectRatio: 1 / 1,
      minCropBoxWidth: 200,
      minCropBoxHeight: 200,
      ready: function () {
        $image.cropper('setCanvasData', canvasData)
        $image.cropper('setCropBoxData', cropBoxData)
      }
    })
  }).on('hidden.bs.modal', function () {
    cropBoxData = $image.cropper('getCropBoxData')
    canvasData = $image.cropper('getCanvasData')
    $image.cropper('destroy')
  })

  $('.js-zoom-in').click(function () {
    $image.cropper('zoom', 0.1)
  })

  $('.js-zoom-out').click(function () {
    $image.cropper('zoom', -0.1)
  })

  /* SCRIPT TO COLLECT THE DATA AND POST TO THE SERVER */

  $('.js-crop-and-upload').click(function () {
    var cropData = $image.cropper('getData')
    $('#id_x').val(cropData.x)
    $('#id_y').val(cropData.y)
    $('#id_height').val(cropData.height)
    $('#id_width').val(cropData.width)
    $('#modalCrop').modal('hide')
    // $("#formUpload").submit();
  })

  // $('.EditCommentBtn').on('click', function (event) {
  //   event.preventDefault()
  //   const editBtn = $(this)
  //   const commentId = editBtn.attr('id').split('-')[1]

  //   const content = $('#comment-content-' + commentId).text()
  //   $('#edit-form-field').val(content)
  //   $('#editForm-' + commentId + ' textarea').val(content)

  //   $('#editDiv-' + commentId).slideToggle()
  //   $('#deleteDiv-' + commentId).slideUp()
  //   $('#repliesDiv-' + commentId).slideUp()
  //   $('#addReplyDiv-' + commentId).slideUp()
  // })

  // $('.DeleteCommentBtn').on('click', function (event) {
  //   event.preventDefault()
  //   const deleteBtn = $(this)
  //   const commentId = deleteBtn.attr('id').split('-')[1]

  //   $('#deleteDiv-' + commentId).slideToggle()
  //   $('#editDiv-' + commentId).slideUp()
  //   $('#repliesDiv-' + commentId).slideUp()
  //   $('#addReplyDiv-' + commentId).slideUp()
  // })

  // $('.repliesBtn').on('click', function (event) {
  //   event.preventDefault()
  //   const repliesBtn = $(this)
  //   const commentId = repliesBtn.attr('id').split('-')[1]
  //   $('#repliesDiv-' + commentId).slideToggle()
  //   $('#editDiv-' + commentId).slideUp()
  //   $('#deleteDiv-' + commentId).slideUp()
  //   $('#addReplyDiv-' + commentId).slideUp()
  // })
  // $('.addReplyBtn').on('click', function (event) {
  //   event.preventDefault()
  //   const deleteBtn = $(this)
  //   const commentId = deleteBtn.attr('id').split('-')[2]

  //   $('#addReplyDiv-' + commentId).slideToggle()
  //   $('#editDiv-' + commentId).slideUp()
  //   $('#deleteDiv-' + commentId).slideUp()
  //   $('#repliesDiv-' + commentId).slideUp()
  // })

  // $('.replyEditCommentBtn').on('click', function (event) {
  //   event.preventDefault()
  //   const editBtn = $(this)
  //   const commentId = editBtn.attr('id').split('-')[2]

  //   const content = $('#reply-content-' + commentId).text()

  //   $('#reply-editForm-' + commentId + ' textarea').val(content)

  //   $('#reply-editDiv-' + commentId).slideToggle()
  //   $('#reply-deleteDiv-' + commentId).slideUp()
  // })

  // $('.replyDeleteCommentBtn').on('click', function (event) {
  //   event.preventDefault()
  //   const deleteBtn = $(this)
  //   const commentId = deleteBtn.attr('id').split('-')[2]

  //   $('#reply-deleteDiv-' + commentId).slideToggle()
  //   // $('#editDiv-'+ commentId ).slideUp();
  })



})
