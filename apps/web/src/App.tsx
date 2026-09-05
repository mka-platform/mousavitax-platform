import { useState } from "react";
import { Ask } from "./pages/Ask";
import { Terms } from "./pages/Terms";
import { ConsultationThread } from "./pages/ConsultationThread";
import { Placeholder } from "./pages/Placeholder";
import { menu, type Role, homePath } from "./config/roles";

const labels: Record<string,string> = { dashboard:"داشبورد", office:"دفتر مشاوره", ask:"پرسش مالیاتی", documents:"اسناد", consultations:"مشاوره‌ها", terms:"شرایط استفاده" };

export function App() {
  const [role, setRole] = useState<Role>("owner");
  const initial = homePath[role].replace("/","");
  const [page, setPage] = useState(initial);
  const items = menu[role];
  const changeRole = (next: Role) => { setRole(next); setPage(homePath[next].replace("/","")); };
  const content = page === "ask" ? <Ask/> : page === "terms" ? <Terms/> : page === "consultations" ? <ConsultationThread draftAction={new URLSearchParams(location.search).get("draftAction") || undefined}/> : <Placeholder title={labels[page] || "پنل"}/>;
  return <div className="shell" dir="rtl"><aside><h2>MKA / MousaviTax</h2><label>نقش فعلی</label><select value={role} onChange={e=>changeRole(e.target.value as Role)}>{Object.keys(menu).map(r=><option key={r} value={r}>{r}</option>)}</select>{items.map(i=><button key={i} onClick={()=>setPage(i)}>{labels[i] || i}</button>)}<small>این انتخاب نقش صرفاً UI است؛ مجوز واقعی توسط Backend اعمال می‌شود.</small></aside>{content}</div>;
}