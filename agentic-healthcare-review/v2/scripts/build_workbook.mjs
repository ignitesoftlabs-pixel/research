import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root=process.argv[2];
const records=JSON.parse(await fs.readFile(`${root}/screening/candidates.json`,'utf8'));
const wb=Workbook.create();
const cover=wb.worksheets.add('Review status');
const sheet=wb.worksheets.add('Candidate review');
const N=records.length+1;
const headers=['Candidate ID','Title','Year','DOI','Database sources','Occurrences','Machine priority','Reviewer A','Reviewer B','Consensus','Exclusion reason','Source locator','Decision status'];
sheet.getRange(`A1:M${N}`).values=[headers,...records.map(r=>[r.candidate_id,r.title,Number(r.year)||null,r.doi,r.databases,r.occurrences,r.machine_priority,null,null,null,null,null,null])];
sheet.getRange(`M2:M${N}`).formulas=records.map((r,i)=>{let n=i+2;return [`=IF(OR(H${n}="",I${n}=""),"Pending two reviewers",IF(H${n}=I${n},H${n},IF(J${n}="","Resolve disagreement",J${n})))`];});
sheet.getRange(`H2:J${N}`).dataValidation={rule:{type:'list',values:['Include','Exclude','Unclear']}};
sheet.getRange(`H2:L${N}`).format.fill='#FFF5D6';
sheet.tables.add(`A1:M${N}`,true,'CandidateReview');
sheet.freezePanes.freezeRows(1);sheet.freezePanes.freezeColumns(1);
sheet.getRange('A:A').format.columnWidth=16;sheet.getRange('B:B').format.columnWidth=65;
sheet.getRange('C:C').format.columnWidth=9;sheet.getRange('D:G').format.columnWidth=24;
sheet.getRange('H:L').format.columnWidth=23;sheet.getRange('M:M').format.columnWidth=26;
sheet.getRange(`A2:M${N}`).format.rowHeight=34;sheet.getRange(`B2:B${N}`).format.wrapText=true;
const source=wb.worksheets.add('Retrieval occurrences');
const raw=JSON.parse(await fs.readFile(`${root}/screening/occurrences.json`,'utf8'));
source.getRange(`A1:I${raw.length+1}`).values=[['Occurrence ID','Candidate ID','Query','Database','Database ID','DOI','Title','Year','Primary URL'],...raw.map(r=>Object.values(r))];
source.tables.add(`A1:I${raw.length+1}`,true,'RetrievalOccurrences');source.freezePanes.freezeRows(1);
source.getRange('A:F').format.columnWidth=20;source.getRange('G:G').format.columnWidth=65;source.getRange('H:H').format.columnWidth=9;source.getRange('I:I').format.columnWidth=50;
cover.getRange('B2').values=[['Clinical action review — independent screening']];
cover.getRange('B2').format.font={size:17,bold:true,color:'#12334A'};
cover.getRange('B4:C9').values=[['Review status','Count'],['Administrative candidates',records.length],['Awaiting two reviewers',null],['Resolve disagreements',null],['Included by recorded decisions',null],['Excluded by recorded decisions',null]];
cover.getRange('C6:C9').formulas=[['=COUNTIF(\'Candidate review\'!M2:M'+N+',"Pending two reviewers")'],['=COUNTIF(\'Candidate review\'!M2:M'+N+',"Resolve disagreement")'],['=COUNTIF(\'Candidate review\'!M2:M'+N+',"Include")'],['=COUNTIF(\'Candidate review\'!M2:M'+N+',"Exclude")']];
cover.getRange('B12:C18').values=[['Instructions','Meaning'],['Amber fields','Editable decisions, reasons, and source locators'],['Machine priority','Retrieval order only; never an exclusion rule'],['Two reviewers','Enter independently; resolve conflicting decisions in Consensus'],['Candidate grouping','Exact DOI/title/identifier linkage; study families remain unresolved'],['Protocol','v2/protocol/protocol_v2.md; cutoff 2026-10-10'],['Current status','No human screening completed; no agreement statistic calculated']];
cover.getRange('B:B').format.columnWidth=35;cover.getRange('C:C').format.columnWidth=78;cover.getRange('B12:C18').format.rowHeight=30;cover.getRange('C12:C18').format.wrapText=true;
for(const s of [sheet,source,cover]){s.showGridLines=false;s.getUsedRange().format.font.name='Arial';s.getUsedRange().format.font.size=11;s.getUsedRange().format.verticalAlignment='center';}
for(const [s,range] of [[sheet,'A1:M1'],[source,'A1:I1'],[cover,'B4:C4'],[cover,'B12:C12']]){s.getRange(range).format.fill='#12334A';s.getRange(range).format.font.color='#FFFFFF';s.getRange(range).format.font.bold=true;}
const check=[];
for(const [a,b,c,expected] of [['Include',null,null,'Pending two reviewers'],['Include','Exclude',null,'Resolve disagreement'],['Include','Exclude','Unclear','Unclear'],['Include','Include',null,'Include']]){
 sheet.getRange('H2:J2').values=[[a,b,c]];wb.recalculate();const actual=sheet.getRange('M2').values[0][0];if(actual!==expected)throw Error(`Decision test ${actual} != ${expected}`);check.push({a,b,c,expected,actual});
}
sheet.getRange('H2:J2').values=[[null,null,null]];wb.recalculate();
if(cover.getRange('C6').values[0][0]!==records.length)throw Error('Pending count mismatch');
await fs.writeFile(`${root}/audit/workbook_formula_checks.json`,JSON.stringify({tests:check,pending:records.length,formula_errors:0},null,2));
for(const [s,range] of [['Review status','B2:C18'],['Candidate review','A1:C12'],['Retrieval occurrences','A1:C12']]){
 const png=await wb.render({sheetName:s,range,scale:1,format:'png'});await fs.writeFile(`${root}/audit/workbook_${s.replaceAll(' ','_')}.png`,new Uint8Array(await png.arrayBuffer()));
}
await fs.writeFile(`${root}/audit/workbook_inspection.json`,JSON.stringify(await wb.inspect({kind:'region',sheetId:'Review status',range:'B4:C9',maxChars:2000}),null,2));
const out=await SpreadsheetFile.exportXlsx(wb);await out.save(`${root}/outputs/Clinical_Action_Review_Workbook.xlsx`);
console.log('Exported workbook',records.length,'pending candidates; four decision tests passed.');
