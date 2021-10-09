<template>
  <div id="page-top">
    <Nav></Nav>
    <Header />
    <ContentArea />
    <Footer />
  </div>
</template>
<script>
import Nav from "@/components/Nav";
import Header from "@/components/Header";
import ContentArea from "@/components/ContentArea";
import Footer from "@/components/Footer";

export default {
  components: {
    Nav,
    Header,
    ContentArea,
    Footer,
  },
};
</script>

<style></style>
