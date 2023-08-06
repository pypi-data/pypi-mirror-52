guiFields.inventory_autocomplete=class InventoryAutocompleteField extends guiFields.fk_multi_autocomplete{toInner(data){let val,value;val=value=data[this.options.name];if(!value){return;}
if(value&&typeof value=="object"){val=value.value;}
if(!val){return;}
if(!isNaN(Number(val))){return val;}
if(val[val.length-1]==","){return val;}
let prefix='./';if(val.substr(0,2)==prefix){return val;}
return prefix+val;}
_prefetchDataOrNot(data){let value=this.toInner(data);if(!isNaN(Number(value))){return true;}
return false;}
prefetchDataOrNot(data){return this._prefetchDataOrNot(data);}
makeLinkOrNot(data){return this._prefetchDataOrNot(data);}};guiFields.playbook_autocomplete=class PlaybookAutocompleteField extends guiFields.fk_autocomplete{_prefetchDataOrNot(data){return false;}
prefetchDataOrNot(data){return this._prefetchDataOrNot(data);}
makeLinkOrNot(data){return this._prefetchDataOrNot(data);}};guiFields.module_autocomplete=class ModuleAutocompleteField extends guiFields.playbook_autocomplete{};guiFields.group_autocomplete=class GroupAutocompleteField extends guiFields.playbook_autocomplete{};guiFields.history_initiator=class HistoryInitiatorField extends guiFields.fk{static get initiatorTypes(){return history_initiator_types;}
getAppropriateQuerySet(data={},querysets=null){let qs=querysets;if(!qs){qs=this.options.additionalProperties.querysets;}
let dict=this.constructor.initiatorTypes;let selected=qs[0];let path=dict[data.initiator_type];if(!path){return selected;}
for(let index=0;index<qs.length;index++){let item=qs[index];let p1=item.url.replace(/^\/|\/$/g,"").split("/");let p2=path.replace(/^\/|\/$/g,"").split("/");if(p1.last==p2.last){selected=item;}}
return selected;}
formatQuerySetUrl(url="",data={},params={}){if(url.indexOf('{')==-1){return url;}
let project=data.project||app.application.$route.params[path_pk_key];if(project&&typeof project=='object'&&project.value){project=project.value;}
let f_obj={};f_obj[path_pk_key]=project;return url.format(f_obj);}};guiFields.one_history_initiator=class OneHistoryInitiatorField extends guiFields.history_initiator{static get mixins(){return super.mixins.concat(gui_fields_mixins.one_history_string,gui_fields_mixins.one_history_initiator);}};guiFields.history_executor=class HistoryExecutorField extends guiFields.fk{makeLinkOrNot(data={}){if(data.initiator_type=='scheduler'){return false;}
return true;}
prefetchDataOrNot(data={}){if(data.initiator_type=='scheduler'){return false;}
return true;}
toRepresent(data={}){if(data.initiator_type=='scheduler'){return'system';}
let value=data[this.options.name];if(value&&typeof value=="object"){return value.prefetch_value;}
return value;}
static get mixins(){return super.mixins.concat(gui_fields_mixins.history_executor);}};guiFields.one_history_executor=class OneHistoryExecutorField extends guiFields.history_executor{static get mixins(){return super.mixins.concat(gui_fields_mixins.one_history_string,gui_fields_mixins.one_history_executor);}};guiFields.ansible_json=class AnsibleJsonField extends guiFields.base{static get mixins(){return super.mixins.concat(gui_fields_mixins.ansible_json);}};guiFields.fk_just_value=class FkJustValueField extends guiFields.fk{static get mixins(){return super.mixins.concat(gui_fields_mixins.fk_just_value);}};guiFields.one_history_string=class OneHistoryStringField extends guiFields.string{static get mixins(){return super.mixins.concat(gui_fields_mixins.one_history_string);}};guiFields.one_history_fk=class OneHistoryFkField extends guiFields.fk{static get mixins(){return super.mixins.concat(gui_fields_mixins.one_history_string,gui_fields_mixins.one_history_fk);}};guiFields.one_history_date_time=class OneHistoryDateTime extends guiFields.date_time{static get mixins(){return super.mixins.concat(gui_fields_mixins.one_history_string);}
toRepresent(data={}){let value=data[this.options.name];if(!value){return;}
return moment(moment.tz(value,window.timeZone)).tz(moment.tz.guess()).format("YYYY-MM-DD HH:mm:ss");}};guiFields.one_history_uptime=class OneHistoryUpTime extends guiFields.uptime{static get mixins(){return super.mixins.concat(gui_fields_mixins.one_history_string);}};guiFields.one_history_revision=class OneHistoryRevision extends guiFields.one_history_string{toRepresent(data={}){let value=data[this.options.name];if(value){return value.substr(0,8);}}};guiFields.one_history_choices=class OneHistoryChoices extends guiFields.choices{static get mixins(){return super.mixins.concat(gui_fields_mixins.one_history_string,gui_fields_mixins.one_history_choices);}};guiFields.one_history_raw_inventory=class OneHistoryRawInventoryField extends guiFields.plain_text{static get mixins(){return super.mixins.concat(gui_fields_mixins.one_history_raw_inventory);}};guiFields.one_history_boolean=class OneHistoryBooleanField extends guiFields.boolean{static get mixins(){return super.mixins.concat(gui_fields_mixins.one_history_string,gui_fields_mixins.one_history_boolean);}};guiFields.one_history_execute_args=class OneHistoryExecuteArgsField extends guiFields.json{static get mixins(){return super.mixins.concat(gui_fields_mixins.one_history_execute_args);}
generateRealFields(value={}){let realFields={};for(let field in value){if(value.hasOwnProperty(field)){let opt={name:field,readOnly:this.options.readOnly||false,title:field,format:'one_history_string',};if(typeof value[field]=='boolean'){opt.format='one_history_boolean';}
realFields[field]=new guiFields[opt.format](opt);}}
return realFields;}};