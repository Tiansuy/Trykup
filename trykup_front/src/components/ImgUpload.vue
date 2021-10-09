<template>
  <div class="rz-picter">
    <img :src="avatar" class="img-avatar" />
    <input
      type="file"
      name="avatar"
      id="uppic"
      accept="image/gif,image/jpeg,image/jpg,image/png"
      @change="changeImage($event)"
      ref="avatarInput"
      class="uppic"
    />
  </div>
</template>

<script>
export default {
  data() {
    return {
      avatar: require("@/assets/img/add.jpg"),
    };
  },
  props: ["label"],
  methods: {
    // to do
    //   uploadFile(file){
    //     axios({})
    //   }

    changeImage(e) {
      var file = e.target.files[0];
      // 上传图片文件到服务器
      //var server_path = uploadFile(file)
      // var server_path = "./path";
      var reader = new FileReader();
      var that = this;
      reader.readAsDataURL(file);
      reader.onload = function () {
        that.avatar = this.result;
        that.$emit("img_upload", this.result, that.label, file);
      };
    },
  },
};
</script>

<style>
.rz-picter {
  height: 3rem;
  width: 6rem;
  margin: 0.3rem auto;
  border: 0.01rem solid #ededed;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.uppic {
  height: 3rem;
  width: 6rem;
  margin: 0 auto;
  opacity: 0;
  z-index: 99999;
}
.img-avatar {
  width: 160px;
  height: 160px;
  position: absolute;
}
</style>
