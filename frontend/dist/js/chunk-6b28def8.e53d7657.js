(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-6b28def8"],{"8dfd":function(e,t,n){"use strict";n.r(t);n("b0c0");var i=n("7a23"),c={class:"p-grid",style:{height:"100vh"}},a={class:"p-col-fixed",style:{width:"50px"}},o={class:"p-col"},l={class:"p-col-12 p-text-left p-text-italic p-m-0 p-px-5"};function r(e,t,n,r,b,s){var u=Object(i["H"])("organisation-sidebar"),d=Object(i["H"])("router-view");return Object(i["z"])(),Object(i["g"])("div",c,[Object(i["k"])("div",a,[Object(i["k"])(u,{links:b.links,name:e.network.name,onReroute:s.goToPage},null,8,["links","name","onReroute"])]),Object(i["k"])("div",o,[Object(i["k"])("div",l,[Object(i["k"])("p",null,Object(i["L"])(e.network.name),1),Object(i["k"])("h3",null,Object(i["L"])(b.pagename||this.$route.meta.breadcrumb[this.$route.meta.breadcrumb.length-1].label),1)]),Object(i["k"])(d)])])}var b=n("5530"),s=n("5502"),u=n("de8f"),d={components:{OrganisationSidebar:u["a"]},data:function(){return{links:[{label:"Overview",icon:"home"},{label:"Campaigns",icon:"chart-bar"},{label:"Methods",icon:"chart-bar"},{label:"Organisations",icon:"cloud"},{label:"Settings",icon:"cog"}],pagename:void 0}},computed:Object(b["a"])({},Object(s["d"])("network",["network"])),methods:{goToPage:function(e){var t;this.pagename=e,this.$router.push({name:"network".concat(e.toLowerCase()),params:{NetworkId:(null===(t=this.network)||void 0===t?void 0:t.id)||0}})}}};d.render=r;t["default"]=d},de8f:function(e,t,n){"use strict";n("b0c0");var i=n("7a23"),c={class:"p-py-5"},a={class:"p-d-flex p-flex-column p-px-5 p-text-left"};function o(e,t,n,o,l,r){var b=Object(i["H"])("Button"),s=Object(i["H"])("Divider"),u=Object(i["H"])("Sidebar");return Object(i["z"])(),Object(i["g"])(i["a"],null,[Object(i["k"])(b,{icon:"pi pi-angle-right",class:"p-button-text",onClick:t[1]||(t[1]=function(e){return l.visibleleft=!0}),style:{"background-color":"#EFEEEE",height:"100%"}}),Object(i["k"])(u,{visible:l.visibleleft,"onUpdate:visible":t[2]||(t[2]=function(e){return l.visibleleft=e}),style:{width:"250px"}},{default:Object(i["R"])((function(){return[Object(i["k"])("div",c,[Object(i["k"])("h3",null,Object(i["L"])(n.name),1),Object(i["k"])(s),Object(i["k"])("div",a,[(Object(i["z"])(!0),Object(i["g"])(i["a"],null,Object(i["F"])(n.links,(function(e){return Object(i["z"])(),Object(i["g"])("div",{key:e.label},[Object(i["k"])(b,{label:e.label,icon:"pi pi-".concat(e.icon),class:"p-button-secondary p-button-text",onClick:function(t){return r.goToPage(e.label)}},null,8,["label","icon","onClick"])])})),128))])])]})),_:1},8,["visible"])],64)}var l={props:{links:{type:Array,default:function(){return[]}},name:{type:String,default:"Name"}},data:function(){return{visibleleft:!1}},methods:{goToPage:function(e){this.$emit("reroute",e)}}};l.render=o;t["a"]=l}}]);
//# sourceMappingURL=chunk-6b28def8.e53d7657.js.map