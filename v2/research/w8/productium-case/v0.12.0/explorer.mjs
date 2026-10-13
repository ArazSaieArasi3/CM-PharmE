// Domain read model for a pinned source extract. No name-based identity merge.
export function search(data,term='') {
 const q=term.trim().toLocaleLowerCase();
 return data.products.filter(p=>[p.id,p.ndc,p.name,p.generic_name,p.organization_name,...p.packages.map(x=>x.ndc)].some(x=>x.toLocaleLowerCase().includes(q)));
}
export function inspect(data,id) {
 const p=data.products.find(p=>p.id===id);
 if(!p) throw new Error('Unknown product reference');
 return {product:p,relations:p.packages.map(pack=>({
  product:p.id,presentation:pack.id,listing:pack.listing,organization:p.organization_id,
  source_record:pack.source_record||null,source_pointer:pack.source_pointer||null,
  source_status:pack.source_record&&pack.source_pointer?'SOURCE_PRESENT':'SOURCE_MISSING',
  status:pack.source_record&&pack.source_pointer?pack.relationship_status:'SOURCE_MISSING_NOT_FALSE',approval:pack.approval_status,
  native_predicates:['presentationOf','listingPresentation','listingResponsibleOrganization']
 }))};
}
export function exportBrief(data,id,exportedAt=new Date().toISOString()) {
 const view=inspect(data,id),p=view.product;
 return {schema_version:'0.12.0',case_version:'0.12.0',brief_kind:'SOURCE_SCOPED_PHARMACEUTICAL_RESEARCH_BRIEF',
  exported_at:exportedAt,source_snapshot:{url:data.policy.source_url,retrieved_at:data.policy.source_retrieved_at,
   sha256:data.policy.raw_source_sha256,data_origin:data.policy.data_origin},
  model_snapshot:{repository:data.policy.cm_repository,commit:data.policy.cm_commit,
   model_sha256:data.policy.cm_model_sha256,status:data.policy.cm_model_status},
  product:{id:p.id,ndc:p.ndc,name:p.name,json_pointer:p.source_pointer},
  organization:{id:p.organization_id,name:p.organization_name,role:p.organization_role,
   identity_scope:data.policy.organization_identity},
  relationships:view.relations,approval_status:'UNKNOWN',manufacturer_status:'NOT_ESTABLISHED',
  distributor_status:'NOT_ESTABLISHED',domain_acceptance:'PENDING',
  scope_note:'A listing relationship reported in this extract is not independent verification of manufacture, distribution, authorization or current availability.'};
}
