<template>
  <div id="example">
    <div class="container">
      <div id="bar">
        <h1>Email Editor (Demo)</h1>

        <label>導入excel
          <input type="file" accept=".xls,.xlsx,.csv" id="file" ref="file" v-on:change="handleFileUpload"/>
          <button v-on:click="submitFile">Upload data</button>
        </label>
        <!-- <button v-on:click="test_excel">Check data</button> -->
        <!-- <button v-on:click="saveDesign">Save Design</button> -->
        <!-- <button v-on:click="exportHtml">Export HTML</button> -->
        <button @click="sendSampleEmail">Send sample mail</button>
        <button @click="sendMails">OK Send mails</button>
      </div>

      <EmailEditor
        :min-height="minHeight"
        :projectId="projectId"
        :locale="locale"
        ref="emailEditor"
        v-on:load="editorLoaded"
        v-on:ready="editorReady"
      />
    </div>
  </div>
</template>

<script>
  import { EmailEditor } from 'vue-email-editor';
  import axios from 'axios';

  export default {
    name: 'exampleView',
    components: {
      EmailEditor,
    },
    data() {
        return {
            minHeight: "100%",
            projectId: 164913,
            locale: "zh-TW",
            file: "",
            excel_id: "",
            excel_data: [],
            mailBody: "base"
        }
    },
    methods: {
      // called when the editor is created
      editorLoaded() {
        console.log('editorLoaded');
        // Pass the template JSON here
        // this.$refs.emailEditor.editor.loadDesign({});
      },
      // called when the editor has finished loading
      editorReady() {
        console.log('editorReady');
      },
      saveDesign() {
        this.$refs.emailEditor.editor.saveDesign((design) => {
          console.log('saveDesign', design);
        });
      },
      exportHtml() {
        this.$refs.emailEditor.editor.exportHtml((data) => {
          // console.log('exportHtml', data);
          console.log(data)
        });
      },
      input_excel() {
        return null
      },
      test_excel() {
        axios.get('http://localhost:8000/files/' + this.excel_id, {
          params: {
            skip: 0,
            limit: 1
          },
          headers: {
            "accept": "application/json",
            "csrfToken": "inuitoko"
          }
        }).then(
          (res) => {
          console.log(res.data);
          this.excel_data = res.data;
          console.log(this.excel_data)
        }).catch(
          (error) => {console.log(error)}
        )
      },
      submitFile() {
        let formData = new FormData();
        formData.append('file', this.file);
        axios.post('http://localhost:8000/files/uploadfile',
          formData,
          {
          // params: {
          //   token: 'inuitoko'
          // },
          headers: {
            'accept': 'application/json',
            'Content-Type': 'multipart/form-data',
            "csrfToken": "inuitoko"
          }
        }).then(
          (res) => {
            console.log(res.data);
            this.excel_id = res.data.file_id;
            window.alert('檔案上傳完成')
          }
        ).catch(
          (error) => {
            console.log(error);
            window.alert(error.response.data.message)
          }
        )
      },
      handleFileUpload() {
        this.file = this.$refs.file.files[0]
      },
      sendSampleEmail() {
        const sampleMail = prompt('請輸入接收信箱');
        const excelId = this.excel_id;
        new Promise((resolve) => {
          this.$refs.emailEditor.editor.exportHtml((data) => {
            resolve(data);
          });
        }).then((mailBody) => {
          console.log("mailBody:", mailBody);
          console.log("sampleMail:", sampleMail);
          console.log("excelId:", excelId);

          axios.post('http://localhost:8000/email/send-sample-email',{
            "commons": {
              "skip": 0,
              "limit": 1
            },
            "mail_request": {
              "file_id": excelId,
              "mail_body": mailBody.html
            },
            "email": sampleMail
          },{
            headers: {
              'accept': 'application/json',
              'Content-Type': 'application/json',
              "csrfToken": "inuitoko"
            }
          }).then((res) => {
            console.log(res.data);
            window.alert('郵件寄出')
          }).catch((error) => {
            console.log(error);
            window.alert(error.response.data.message)
          });
        }).catch((error) => {
          console.log(error);
        });
      },
      sendMails() {
        const check = confirm('請確認傳入文件的欄位包含[email]及[subject]');
        if (check) {
          const excelId = this.excel_id;
          new Promise((resolve) => {
            this.$refs.emailEditor.editor.exportHtml((data) => {
              resolve(data);
            });
          }).then((mailBody) => {
            console.log("mailBody:", mailBody);
            console.log("excelId:", excelId);

            axios.post('http://localhost:8000/email/send-emails',{
              "mail_request": {
                "file_id": excelId,
                "mail_body": mailBody.html
              }
            },{
              headers: {
                'accept': 'application/json',
                'Content-Type': 'application/json',
                "csrfToken": "inuitoko"
              }
            }).then((res) => {
              console.log(res.data);
              window.alert('郵件寄出')
            }).catch((error) => {
              console.log(error);
              window.alert(error.response.data.message)
            });
          }).catch((error) => {
            console.log(error);
          });
        } else {
          console.log("放棄送出信件")
        }
      }
    },
  };
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: Arial, "Helvetica Neue", Helvetica, sans-serif;
}

#app, #example {
  height: 100%;
}

#example .container {
  display: flex;
  flex-direction: column;
  position: relative;
  height: 100%;
}

#bar {
  flex: 1;
  background-color: #40B883;
  color: #FFF;
  padding: 10px;
  display: flex;
  max-height: 40px;
}

#bar h1 {
  flex: 1;
  font-size: 16px;
  text-align: left;
}

#bar button {
  flex: 1;
  padding: 10px;
  margin-left: 10px;
  font-size: 14px;
  font-weight: bold;
  background-color: #000;
  color: #FFF;
  border: 0px;
  max-width: 150px;
  cursor: pointer;
}
</style>