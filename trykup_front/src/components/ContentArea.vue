<template>
  <div>
    <section id="scroll">
      <div class="container px-5">
        <div class="row gx-5 align-items-center">
          <div class="col-lg-2 topper">
            <div class="p-3">
              <h6 class="box-tip topper fcenter">素颜照</h6>
              <ImgUpload label="naive" @img_upload="getImgUrl" />
            </div>
          </div>
          <div class="col-lg-1">
            <div class="p-5 fcenter">
              <h6 class="icon-mix">+</h6>
            </div>
          </div>
          <div class="col-lg-3 topper">
            <div class="p-5">
              <h6 class="box-tip topper fcenter">带妆照</h6>
              <ImgUpload label="refer" @img_upload="getImgUrl" />
            </div>
          </div>
          <div class="col-lg-1">
            <div class="p-1 fr-center">
              <h6 class="icon-mix">=</h6>
              <button
                @click="doMix"
                class="btn btn-secondary wider"
                type="button"
              >
                合成
              </button>
            </div>
          </div>
          <div class="col-lg-4">
            <div class="p-5">
              <img
                class="img-fluid rounded-circle"
                :src="transfered.length>0?transfered:require('@/assets/img/default.jpg')"
                alt="..."
              />
            </div>
          </div>
          <div class="col-lg-1" v-if="res_data.length > 0">
            <div class="p-5 dropdown fcenter">
              <button
                class="btn btn-info dropdown-toggle"
                type="button"
                id="dropdownMenuButton1"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                Download
              </button>
              <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
                <li>
                  <a class="dropdown-item" @click="download('png')" href="#">PNG</a>
                </li>
                <li><a class="dropdown-item" @click="download('jpg')" href="#">JPG</a></li>
                <li><a class="dropdown-item" @click="download('jpeg')" href="#">JPEG</a></li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import ImgUpload from "@/components/ImgUpload";
import axios from "axios";

export default {
  components: { ImgUpload },
  data() {
    return {
      img_naive: "123",
      img_naive_data: {},
      img_refer: "",
      img_refer_data: {},
      transfered:"",
      res_data: "w",
    };
  },
  methods: {
    getImgUrl(url, label, data) {
      if (label === "naive") {
        this.img_naive = url;
        this.img_naive_data = data;
      } else {
        this.img_refer = url;
        this.img_refer_data = data;
      }
    },
    doMix() {
      if (this.img_naive.length == 0 || this.img_refer.length == 0) {
        alert("请先上传两张图片");
        return;
      }
      let that = this;
      console.log(that.img_naive_data);
      let param = new FormData();
      param.append("source",that.img_naive_data)
      param.append("refer",that.img_refer_data)
      //axios请求后台得到图片以及下载链接
      axios({
        method: "post",
        url: "http://localhost:5000/predict2",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        data: param
      }).then(res=>{
          console.log(res);
          that.transfered=res.data.transfered
      })
    },
    download(type) {
      console.log(type);
    //   alert(type)
      axios({
        method: "get",
        url: "http://localhost:5000/download",
        responseType: 'arraybuffer',
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        params:{
            type:type
        }
      }).then(res=>{
            console.log(res);
            const blob = new Blob([res.data])
            const link = document.createElement('a')
            link.download = "迁移结果."+type
            link.style.display = 'none'
            link.href = URL.createObjectURL(blob)
            document.body.appendChild(link)
            link.click() // 执行下载
            URL.revokeObjectURL(link.href)  // 释放 bolb 对象
            document.body.removeChild(link) // 下载完成移除元素
        }).catch(function (error) {
            console.log(error)
        })
    },
  },
};
</script>

<style>
.topper {
  margin-bottom: 100px;
}
.lefter {
  left: -60px;
}
.look {
  border: 2px solid #000;
}
.fcenter {
  display: flex;
  justify-content: center;
}
.fr-center {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.wider {
  width: 75px;
  color: #fff !important;
}
</style>
