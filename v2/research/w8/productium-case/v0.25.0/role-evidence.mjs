// Source observations, not inferred pharmaceutical activities or native role types.
export function roleEvidence(data,product) {
 const raw=product.source_envelope||{},open=raw.openfda||{};
 const problems=[];
 const pointer=typeof product.source_pointer==='string'&&/^\/results\/\d+$/.test(product.source_pointer)?product.source_pointer:null;
 const digest=data.policy?.raw_source_sha256;
 const provenance=pointer&&typeof digest==='string'&&/^[a-f0-9]{64}$/.test(digest);
 const label=typeof raw.labeler_name==='string'&&raw.labeler_name.trim()?raw.labeler_name:null;
 if(!provenance)problems.push('SOURCE_LOCATOR_INCOMPLETE');
 if(raw.product_ndc!==product.ndc)problems.push('PRODUCT_REFERENCE_MISMATCH');
 if(label===null)problems.push('LABELER_NAME_MISSING_OR_INVALID');
 if(label!==null&&label!==product.organization_name)problems.push('LABELER_PROJECTION_MISMATCH');
 let names=[];
 // FDA reference declares string values; API envelopes may contain harmonized arrays.
 // Preserve the raw envelope and every nonblank observed string with its exact pointer.
 const value=open.manufacturer_name;
 if(typeof value==='string'){
  if(value.trim())names=[{value,json_pointer:pointer?pointer+'/openfda/manufacturer_name':null}];
  else problems.push('MANUFACTURER_FIELD_INVALID');
 }else if(Array.isArray(value)){
  names=value.flatMap((v,i)=>typeof v==='string'&&v.trim()?[{value:v,json_pointer:pointer?pointer+'/openfda/manufacturer_name/'+i:null}]:[]);
  if(names.length!==value.length)problems.push('MANUFACTURER_FIELD_INVALID');
 }else if(value!==undefined&&value!==null)problems.push('MANUFACTURER_FIELD_INVALID');
 const unique=[...new Set(names.map(x=>x.value))];
 const comparison=unique.length>1?'MULTIPLE_NAMES_REVIEW':unique.length===0?'NO_REPORTED_NAME':label===unique[0]?'EXACT_TEXT_AGREEMENT':'DIFFERENT_TEXT_REVIEW';
 if(['MULTIPLE_NAMES_REVIEW','DIFFERENT_TEXT_REVIEW'].includes(comparison))problems.push(comparison);
 const listingOK=!!provenance&&label!==null&&label===product.organization_name&&raw.product_ndc===product.ndc;
 return {
  contract_version:'0.25.0',source_locator_present:!!provenance,
  source_snapshot_sha256:provenance?digest:null,source_retrieved_at:data.policy?.source_retrieved_at||null,
  labeler:{name:label,json_pointer:pointer?pointer+'/labeler_name':null,status:listingOK?'SOURCE_REPORTED_LISTING_RESPONSIBILITY':'REVIEW_REQUIRED',organization_reference:product.organization_id||null},
  harmonized_manufacturer:{observations:names,status:names.length?(provenance?'SOURCE_REPORTED_FIELD':'SOURCE_LOCATOR_MISSING'):'NOT_REPORTED',comparison_to_labeler:comparison},
  distributor:{status:'NOT_ESTABLISHED_FROM_NDC_FIELDS'},
  native_role_projection:{listing_responsibility:listingOK?'RETAINED_SOURCE_SCOPED':'WITHHELD_PENDING_REVIEW',ManufacturerRole:'NOT_ASSERTED',WholesaleDistributorRole:'NOT_ASSERTED'},
  approval_status:'UNKNOWN',review_reasons:problems,
  interpretation:'Source field values are retained. Text agreement does not establish entity identity, manufacturing activity, wholesale distribution, authorization or approval.'
 };
}
