============================================================
📄 src/index.css
============================================================
@tailwind base;
@tailwind components;
@tailwind utilities;

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

@layer base {
  :root {
    --background: 222 47% 6%;
    --foreground: 210 40% 96%;

    --card: 222 40% 10%;
    --card-foreground: 210 40% 96%;

    --popover: 222 40% 10%;
    --popover-foreground: 210 40% 96%;

    --primary: 239 84% 67%;
    --primary-foreground: 0 0% 100%;

    --secondary: 222 30% 16%;
    --secondary-foreground: 210 40% 96%;

    --muted: 222 30% 14%;
    --muted-foreground: 215 20% 55%;

    --accent: 239 84% 67%;
    --accent-foreground: 0 0% 100%;

    --destructive: 0 84% 60%;
    --destructive-foreground: 0 0% 100%;

    --border: 222 30% 18%;
    --input: 222 30% 18%;
    --ring: 239 84% 67%;

    --radius: 0.75rem;

    --sidebar-background: 222 40% 8%;
    --sidebar-foreground: 210 40% 96%;
    --sidebar-primary: 239 84% 67%;
    --sidebar-primary-foreground: 0 0% 100%;
    --sidebar-accent: 222 30% 14%;
    --sidebar-accent-foreground: 210 40% 96%;
    --sidebar-border: 222 30% 18%;
    --sidebar-ring: 239 84% 67%;

    --gradient-primary: linear-gradient(135deg, hsl(239 84% 67%), hsl(260 84% 60%));
    --gradient-card: linear-gradient(135deg, hsl(222 40% 10%), hsl(222 30% 14%));
    --shadow-glow: 0 0 30px hsl(239 84% 67% / 0.15);
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground font-sans antialiased;
    font-family: 'Inter', sans-serif;
  }
}

@layer utilities {
  .page-transition {
    @apply animate-fade-in;
  }
  .glass-card {
    @apply bg-card/80 backdrop-blur-xl border border-border/50 rounded-2xl;
    box-shadow: var(--shadow-glow);
  }
  .glow-border {
    @apply border border-primary/30;
    box-shadow: 0 0 20px hsl(239 84% 67% / 0.1), inset 0 0 20px hsl(239 84% 67% / 0.05);
  }
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slide-up {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}


============================================================
📄 tailwind.config.ts
============================================================
import type { Config } from "tailwindcss";

export default {
  darkMode: ["class"],
  content: ["./pages/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./app/**/*.{ts,tsx}", "./src/**/*.{ts,tsx}"],
  prefix: "",
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        sidebar: {
          DEFAULT: "hsl(var(--sidebar-background))",
          foreground: "hsl(var(--sidebar-foreground))",
          primary: "hsl(var(--sidebar-primary))",
          "primary-foreground": "hsl(var(--sidebar-primary-foreground))",
          accent: "hsl(var(--sidebar-accent))",
          "accent-foreground": "hsl(var(--sidebar-accent-foreground))",
          border: "hsl(var(--sidebar-border))",
          ring: "hsl(var(--sidebar-ring))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
        "fade-in": {
          from: { opacity: "0", transform: "translateY(12px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
        "slide-up": {
          from: { opacity: "0", transform: "translateY(30px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
        "float": {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-6px)" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "fade-in": "fade-in 0.5s ease-out both",
        "slide-up": "slide-up 0.6s ease-out both",
        "float": "float 3s ease-in-out infinite",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
} satisfies Config;


============================================================
📄 src/main.tsx
============================================================
import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import "./index.css";

createRoot(document.getElementById("root")!).render(<App />);


============================================================
📄 src/App.tsx
============================================================
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { LangProvider } from "@/lib/LangContext";
import Sidebar from "@/components/Sidebar";
import HomePage from "@/pages/HomePage";
import GeneratorPage from "@/pages/GeneratorPage";
import FeedbackPage from "@/pages/FeedbackPage";
import AuthorsPage from "@/pages/AuthorsPage";
import NotFound from "@/pages/NotFound";

const App = () => (
  <LangProvider>
    <BrowserRouter>
      <div className="flex min-h-screen">
        <Sidebar />
        <main className="flex-1 ml-64">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/generator" element={<GeneratorPage />} />
            <Route path="/feedback" element={<FeedbackPage />} />
            <Route path="/authors" element={<AuthorsPage />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  </LangProvider>
);

export default App;


============================================================
📄 src/lib/translations.ts
============================================================
export type Lang = "Русский" | "English" | "Қазақша";
export type PageKey = "home" | "generator" | "feedback" | "authors";

export const translations: Record<Lang, Record<string, any>> = {
  "Русский": {
    nav: { home: "Главная", generator: "Генератор", feedback: "Отзывы", authors: "Авторы" },
    subtitle: "Ваш надежный ИИ-помощник для малого бизнеса.",
    runBtn: "ЗАПУСТИТЬ ГЕНЕРАТОР",
    genHeader: "Настройка шаблона",
    docType: "Выберите тип документа:",
    address: "Юридические адреса, контакты и банковские реквизиты сторон (IBAN, Банк)",
    submit: "СОЗДАТЬ ДОКУМЕНТ",
    download: "📥 СКАЧАТЬ WORD (.DOCX)",
    feedbackTitle: "Обратная связь",
    name: "Имя",
    review: "Ваш отзыв",
    send: "Отправить",
    thanks: "Спасибо за отзыв!",
    authors: "Авторы проекта",
    city: "г. Астана",
    docs: {
      labor: "Трудовой договор (Двуязычный Каз/Рус)",
      prop: "Договор купли-продажи имущества",
      rent: "Договор аренды помещения",
      serv: "Договор об оказании услуг",
      car: "Договор купли-продажи ТС (Авто)",
    },
    fields: {
      p1_labor: "Работодатель (Название + БИН)", p2_labor: "Работник (ФИО + ИИН)",
      p1_prop: "Продавец (ФИО/Организация)", p2_prop: "Покупатель (ФИО/Организация)",
      p1_rent: "Арендодатель (ФИО/Организация)", p2_rent: "Арендатор (ФИО/Организация)",
      p1_serv: "Заказчик (ФИО/Организация)", p2_serv: "Исполнитель (ФИО/Организация)",
      p1_car: "Продавец ТС (ФИО + ИИН)", p2_car: "Покупатель ТС (ФИО + ИИН)",
      d1_labor: "Должность работника", d2_labor: "Оклад (цифрами и прописью)", d3_labor: "Срок договора",
      d1_prop: "Описание имущества", d2_prop: "Стоимость имущества", d3_prop: "Срок передачи",
      d1_rent: "Адрес помещения", d2_rent: "Арендная плата", d3_rent: "Срок аренды",
      d1_serv: "Описание услуг", d2_serv: "Сумма договора", d3_serv: "Срок оказания",
      d1_car: "Марка, Модель, Год", d2_car: "Цена авто", d3_car: "Гос. номер и VIN код",
    },
  },
  "English": {
    nav: { home: "Home", generator: "Generator", feedback: "Feedback", authors: "Authors" },
    subtitle: "Your reliable AI assistant for small businesses.",
    runBtn: "LAUNCH GENERATOR",
    genHeader: "Template Setup",
    docType: "Select document type:",
    address: "Legal addresses, contacts and bank details (IBAN, Bank)",
    submit: "CREATE DOCUMENT",
    download: "📥 DOWNLOAD WORD (.DOCX)",
    feedbackTitle: "Feedback",
    name: "Name",
    review: "Your review",
    send: "Submit",
    thanks: "Thank you for your feedback!",
    authors: "Project Authors",
    city: "Astana city",
    docs: {
      labor: "Labor Contract (Bilingual Kaz/Rus)",
      prop: "Property Sale Agreement",
      rent: "Lease Agreement",
      serv: "Services Agreement",
      car: "Vehicle Sale Agreement",
    },
    fields: {
      p1_labor: "Employer (Company Name + BIN)", p2_labor: "Employee (Name + IIN)",
      p1_prop: "Seller (Name/Company)", p2_prop: "Buyer (Name/Company)",
      p1_rent: "Landlord (Name/Company)", p2_rent: "Tenant (Name/Company)",
      p1_serv: "Customer (Name/Company)", p2_serv: "Contractor (Name/Company)",
      p1_car: "Seller (Name + IIN)", p2_car: "Buyer (Name + IIN)",
      d1_labor: "Employee Position", d2_labor: "Salary (in words and figures)", d3_labor: "Contract term",
      d1_prop: "Property description", d2_prop: "Property cost", d3_prop: "Transfer deadline",
      d1_rent: "Premises address", d2_rent: "Monthly rent", d3_rent: "Lease term",
      d1_serv: "Services description", d2_serv: "Contract amount", d3_serv: "Deadline",
      d1_car: "Make, Model, Year", d2_car: "Car price", d3_car: "Plate number & VIN",
    },
  },
  "Қазақша": {
    nav: { home: "Басты бет", generator: "Генератор", feedback: "Пікірлер", authors: "Авторлар" },
    subtitle: "Шағын бизнеске арналған сенімді AI көмекшісі.",
    runBtn: "ГЕНЕРАТОРДЫ ІСКЕ ҚОСУ",
    genHeader: "Үлгіні баптау",
    docType: "Құжат түрін таңдаңыз:",
    address: "Заңды мекенжайлар, байланыстар және банк деректемелері (IBAN, Банк)",
    submit: "ҚҰЖАТТЫ ҚҰРУ",
    download: "📥 WORD ЖҮКТЕУ (.DOCX)",
    feedbackTitle: "Кері байланыс",
    name: "Атыңыз",
    review: "Пікіріңіз",
    send: "Жіберу",
    thanks: "Пікіріңіз үшін рахмет!",
    authors: "Жоба авторлары",
    city: "Астана қ.",
    docs: {
      labor: "Еңбек шарты (Екі тілде Қаз/Орыс)",
      prop: "Сатып алу-сату шарты",
      rent: "Жалдау шарты",
      serv: "Қызмет көрсету шарты",
      car: "Көлік құралын сатып алу-сату шарты",
    },
    fields: {
      p1_labor: "Жұмыс беруші (Атауы + БСН)", p2_labor: "Жұмыскер (ТАӘ + ЖСН)",
      p1_prop: "Сатушы (ТАӘ/Ұйым)", p2_prop: "Сатып алушы (ТАӘ/Ұйым)",
      p1_rent: "Жалға беруші (ТАӘ/Ұйым)", p2_rent: "Жалға алушы (ТАӘ/Ұйым)",
      p1_serv: "Тапсырыс беруші (ТАӘ/Ұйым)", p2_serv: "Орындаушы (ТАӘ/Ұйым)",
      p1_car: "Көлік сатушысы (ТАӘ + ЖСН)", p2_car: "Көлік сатып алушысы (ТАӘ + ЖСН)",
      d1_labor: "Қызметкердің лауазымы", d2_labor: "Жалақы мөлшері", d3_labor: "Шарт мерзімі",
      d1_prop: "Мүліктің сипаттамасы", d2_prop: "Мүліктің құны", d3_prop: "Тапсыру мерзімі",
      d1_rent: "Үй-жайдың мекенжайы", d2_rent: "Жалдау ақысы", d3_rent: "Жалдау мерзімі",
      d1_serv: "Қызметтердің сипаттамасы", d2_serv: "Шарт сомасы", d3_serv: "Мерзімі",
      d1_car: "Маркасы, Моделі, Жылы", d2_car: "Көлік құны", d3_car: "Мемлекеттік нөмір және VIN",
    },
  },
};


============================================================
📄 src/lib/docx-generator.ts
============================================================
import { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType } from "docx";
import type { Lang } from "./translations";

export interface DocData {
  p1: string;
  p2: string;
  d1: string;
  d2: string;
  d3: string;
  addr: string;
}

const titles: Record<Lang, Record<string, string>> = {
  "Русский": { prop: "ДОГОВОР КУПЛИ-ПРОДАЖИ", rent: "ДОГОВОР АРЕНДЫ", serv: "ДОГОВОР ОБ ОКАЗАНИИ УСЛУГ", car: "ДОГОВОР КУПЛИ-ПРОДАЖИ ТС" },
  "English": { prop: "SALE AND PURCHASE AGREEMENT", rent: "LEASE AGREEMENT", serv: "SERVICES AGREEMENT", car: "VEHICLE SALE AGREEMENT" },
  "Қазақша": { prop: "САТЫП АЛУ-САТУ ШАРТЫ", rent: "ЖАЛДАУ ШАРТЫ", serv: "ҚЫЗМЕТ КӨРСЕТУ ШАРТЫ", car: "КӨЛІК ҚҰРАЛЫН САТЫП АЛУ-САТУ ШАРТЫ" },
};

const roles: Record<Lang, Record<string, [string, string]>> = {
  "Русский": { prop: ["Продавец", "Покупатель"], rent: ["Арендодатель", "Арендатор"], serv: ["Заказчик", "Исполнитель"], car: ["Продавец", "Покупатель"] },
  "English": { prop: ["Seller", "Buyer"], rent: ["Landlord", "Tenant"], serv: ["Customer", "Contractor"], car: ["Seller", "Buyer"] },
  "Қазақша": { prop: ["Сатушы", "Сатып алушы"], rent: ["Жалға беруші", "Жалға алушы"], serv: ["Тапсырыс беруші", "Орындаушы"], car: ["Сатушы", "Сатып алушы"] },
};

const cityNames: Record<Lang, string> = { "Русский": "г. Астана", "English": "Astana city", "Қазақша": "Астана қ." };

function introText(lang: Lang, docId: string, data: DocData): string {
  const [r1, r2] = roles[lang][docId];
  if (lang === "Русский") return `${data.p1} (далее - ${r1}), с одной стороны, и ${data.p2} (далее - ${r2}), с другой стороны, заключили настоящий договор о нижеследующем:`;
  if (lang === "English") return `${data.p1} (hereinafter - ${r1}), on the one part, and ${data.p2} (hereinafter - ${r2}), on the other part, have concluded this agreement as follows:`;
  return `Бір тараптан ${data.p1} (бұдан әрі - ${r1}), және екінші тараптан ${data.p2} (бұдан әрі - ${r2}), осы шартты жасасты:`;
}

export async function createDocx(docId: string, data: DocData, lang: Lang): Promise<Blob> {
  const dateStr = new Date().toLocaleDateString("ru-RU");
  const children: Paragraph[] = [];

  if (docId === "labor") {
    children.push(
      new Paragraph({ heading: HeadingLevel.HEADING_1, alignment: AlignmentType.CENTER, children: [new TextRun({ text: "ЕҢБЕК ШАРТЫ / ТРУДОВОЙ ДОГОВОР", bold: true })] }),
      new Paragraph({ children: [new TextRun(`Астана қ. / г. Астана\t\t\t\t${dateStr} ж/г.`)] }),
      new Paragraph({ children: [new TextRun(`\nРаботодатель / Жұмыс беруші: ${data.p1}\nРаботник / Жұмыскер: ${data.p2}`)] }),
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("1. Предмет / Шарттың мәні")] }),
      new Paragraph({ children: [new TextRun(`Принять на работу на должность / Лауазымы: ${data.d1}`)] }),
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("2. Оплата и Сроки / Төлем және Мерзімдері")] }),
      new Paragraph({ children: [new TextRun(`Оклад / Жалақы: ${data.d2} KZT.\nСрок / Мерзімі: ${data.d3}`)] }),
    );
  } else {
    children.push(
      new Paragraph({ heading: HeadingLevel.HEADING_1, alignment: AlignmentType.CENTER, children: [new TextRun({ text: titles[lang][docId], bold: true })] }),
      new Paragraph({ children: [new TextRun(`${cityNames[lang]}\t\t\t\t${dateStr}`)] }),
      new Paragraph({ spacing: { before: 200 }, children: [new TextRun(introText(lang, docId, data))] }),
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("1.")] }),
      new Paragraph({ children: [new TextRun(data.d1)] }),
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("2.")] }),
      new Paragraph({ children: [new TextRun(`${data.d2}\n${data.d3}`)] }),
      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("3.")] }),
      new Paragraph({ children: [new TextRun(data.addr)] }),
    );
  }

  const doc = new Document({
    sections: [{ properties: {}, children }],
  });

  return await Packer.toBlob(doc);
}


============================================================
📄 src/lib/LangContext.tsx
============================================================
import { createContext, useContext, useState, type ReactNode } from "react";
import type { Lang } from "./translations";
import { translations } from "./translations";

interface LangCtx {
  lang: Lang;
  setLang: (l: Lang) => void;
  t: Record<string, any>;
}

const Ctx = createContext<LangCtx>(null!);

export function LangProvider({ children }: { children: ReactNode }) {
  const [lang, setLang] = useState<Lang>("Русский");
  return <Ctx.Provider value={{ lang, setLang, t: translations[lang] }}>{children}</Ctx.Provider>;
}

export const useLang = () => useContext(Ctx);


============================================================
📄 src/components/Sidebar.tsx
============================================================
import { useLocation, useNavigate } from "react-router-dom";
import { useLang } from "@/lib/LangContext";
import type { Lang } from "@/lib/translations";
import { FileText, Home, MessageSquare, Users, Globe } from "lucide-react";

const langs: Lang[] = ["Русский", "English", "Қазақша"];

const navItems = [
  { key: "home", path: "/", icon: Home },
  { key: "generator", path: "/generator", icon: FileText },
  { key: "feedback", path: "/feedback", icon: MessageSquare },
  { key: "authors", path: "/authors", icon: Users },
] as const;

export default function Sidebar() {
  const { lang, setLang, t } = useLang();
  const location = useLocation();
  const navigate = useNavigate();
  const now = new Date();

  return (
    <aside className="fixed left-0 top-0 h-full w-64 bg-card/60 backdrop-blur-xl border-r border-border/50 flex flex-col z-50">
      <div className="p-6 border-b border-border/50">
        <h1 className="text-xl font-bold text-foreground tracking-tight">📝 EasyDoc AI</h1>
        <p className="text-xs text-muted-foreground mt-1">{now.toLocaleDateString("ru-RU")}</p>
      </div>

      <div className="px-4 py-3 border-b border-border/50">
        <div className="flex items-center gap-2 text-muted-foreground text-xs mb-2">
          <Globe className="w-3 h-3" /> Language
        </div>
        <select
          value={lang}
          onChange={(e) => setLang(e.target.value as Lang)}
          className="w-full bg-secondary text-foreground text-sm rounded-lg px-3 py-2 border border-border/50 focus:outline-none focus:ring-1 focus:ring-primary"
        >
          {langs.map((l) => (
            <option key={l} value={l}>{l}</option>
          ))}
        </select>
      </div>

      <nav className="flex-1 px-3 py-4 space-y-1">
        {navItems.map(({ key, path, icon: Icon }) => {
          const active = location.pathname === path;
          return (
            <button
              key={key}
              onClick={() => navigate(path)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 ${
                active
                  ? "bg-primary/15 text-primary"
                  : "text-muted-foreground hover:text-foreground hover:bg-secondary/60"
              }`}
            >
              <Icon className="w-4 h-4" />
              {t.nav[key]}
            </button>
          );
        })}
      </nav>

      <div className="p-4 border-t border-border/50 text-xs text-muted-foreground text-center">
        EasyDoc AI © {now.getFullYear()} | Astana
      </div>
    </aside>
  );
}


============================================================
📄 src/pages/HomePage.tsx
============================================================
import { useNavigate } from "react-router-dom";
import { useLang } from "@/lib/LangContext";
import { ArrowRight, FileText, Zap, Globe } from "lucide-react";

export default function HomePage() {
  const { t } = useLang();
  const navigate = useNavigate();

  const features = [
    { icon: FileText, title: "5 типов", desc: "договоров" },
    { icon: Globe, title: "3 языка", desc: "RU / EN / KZ" },
    { icon: Zap, title: "Мгновенно", desc: "генерация DOCX" },
  ];

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 page-transition">
      <div className="text-center max-w-2xl" style={{ animationDelay: "0.1s" }}>
        <div className="inline-flex items-center gap-2 bg-primary/10 text-primary text-sm font-medium px-4 py-2 rounded-full mb-8 animate-fade-in">
          <Zap className="w-4 h-4" /> EasyDoc AI
        </div>

        <h1 className="text-5xl md:text-6xl font-extrabold text-foreground leading-tight animate-fade-in" style={{ animationDelay: "0.15s" }}>
          EasyDoc <span className="text-primary">AI</span>
        </h1>

        <p className="text-lg text-muted-foreground mt-4 animate-fade-in" style={{ animationDelay: "0.25s" }}>
          {t.subtitle}
        </p>

        <button
          onClick={() => navigate("/generator")}
          className="mt-8 inline-flex items-center gap-2 bg-primary text-primary-foreground px-8 py-4 rounded-2xl font-semibold text-base hover:brightness-110 transition-all duration-200 hover:scale-105 animate-fade-in"
          style={{ animationDelay: "0.35s" }}
        >
          {t.runBtn}
          <ArrowRight className="w-5 h-5" />
        </button>
      </div>

      <div className="grid grid-cols-3 gap-6 mt-16 max-w-lg w-full animate-fade-in" style={{ animationDelay: "0.45s" }}>
        {features.map((f, i) => (
          <div key={i} className="glass-card p-5 text-center">
            <f.icon className="w-6 h-6 text-primary mx-auto mb-2" />
            <p className="text-foreground font-semibold text-sm">{f.title}</p>
            <p className="text-muted-foreground text-xs">{f.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}


============================================================
📄 src/pages/GeneratorPage.tsx
============================================================
import { useState } from "react";
import { useLang } from "@/lib/LangContext";
import { createDocx, type DocData } from "@/lib/docx-generator";
import { Download, Sparkles } from "lucide-react";

const docKeys = ["labor", "prop", "rent", "serv", "car"] as const;

export default function GeneratorPage() {
  const { lang, t } = useLang();
  const [docId, setDocId] = useState<string>("labor");
  const [form, setForm] = useState({ p1: "", p2: "", d1: "", d2: "", d3: "", addr: "" });
  const [generating, setGenerating] = useState(false);
  const [blob, setBlob] = useState<Blob | null>(null);

  const set = (k: string, v: string) => setForm((f) => ({ ...f, [k]: v }));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.p1 || !form.p2) return;
    setGenerating(true);
    try {
      const b = await createDocx(docId, form as DocData, lang);
      setBlob(b);
    } finally {
      setGenerating(false);
    }
  };

  const handleDownload = () => {
    if (!blob) return;
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${docId}_${form.p2 || "document"}.docx`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const inputCls = "w-full bg-secondary/60 text-foreground text-sm rounded-xl px-4 py-3 border border-border/50 focus:outline-none focus:ring-2 focus:ring-primary/40 transition-all placeholder:text-muted-foreground/60";

  return (
    <div className="min-h-screen px-6 py-10 page-transition max-w-3xl mx-auto">
      <h2 className="text-2xl font-bold text-foreground mb-8 animate-fade-in">{t.genHeader}</h2>

      <div className="glass-card p-6 mb-6 animate-fade-in" style={{ animationDelay: "0.1s" }}>
        <label className="text-sm text-muted-foreground mb-2 block">{t.docType}</label>
        <select
          value={docId}
          onChange={(e) => { setDocId(e.target.value); setBlob(null); }}
          className={inputCls}
        >
          {docKeys.map((k) => (
            <option key={k} value={k}>{t.docs[k]}</option>
          ))}
        </select>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4 animate-fade-in" style={{ animationDelay: "0.2s" }}>
        <div className="glass-card p-6 space-y-4">
          <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">1. Стороны</p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input className={inputCls} placeholder={t.fields[`p1_${docId}`]} value={form.p1} onChange={(e) => set("p1", e.target.value)} />
            <input className={inputCls} placeholder={t.fields[`p2_${docId}`]} value={form.p2} onChange={(e) => set("p2", e.target.value)} />
          </div>
        </div>

        <div className="glass-card p-6 space-y-4">
          <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">2. Детали</p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input className={inputCls} placeholder={t.fields[`d1_${docId}`]} value={form.d1} onChange={(e) => set("d1", e.target.value)} />
            <input className={inputCls} placeholder={t.fields[`d2_${docId}`]} value={form.d2} onChange={(e) => set("d2", e.target.value)} />
          </div>
          <input className={inputCls} placeholder={t.fields[`d3_${docId}`]} value={form.d3} onChange={(e) => set("d3", e.target.value)} />
          <textarea className={inputCls + " min-h-[80px] resize-none"} placeholder={t.address} value={form.addr} onChange={(e) => set("addr", e.target.value)} />
        </div>

        <button
          type="submit"
          disabled={generating || !form.p1 || !form.p2}
          className="w-full bg-primary text-primary-foreground py-4 rounded-2xl font-semibold text-sm hover:brightness-110 transition-all disabled:opacity-40 flex items-center justify-center gap-2"
        >
          <Sparkles className="w-4 h-4" />
          {generating ? "..." : t.submit}
        </button>
      </form>

      {blob && (
        <div className="mt-6 glass-card p-6 glow-border animate-fade-in text-center">
          <p className="text-sm text-muted-foreground mb-4">✅ Документ готов!</p>
          <button
            onClick={handleDownload}
            className="inline-flex items-center gap-2 bg-primary text-primary-foreground px-6 py-3 rounded-xl font-semibold text-sm hover:brightness-110 transition-all"
          >
            <Download className="w-4 h-4" />
            {t.download}
          </button>
        </div>
      )}
    </div>
  );
}


============================================================
📄 src/pages/FeedbackPage.tsx
============================================================
import { useState } from "react";
import { useLang } from "@/lib/LangContext";
import { Star } from "lucide-react";

const reviews = [
  { name: 'Айдос, ИП "AlmatyTech"', text: "Отличный генератор! Сэкономил кучу времени на договорах аренды.", wish: "Добавьте возможность загружать свои собственные шаблоны." },
  { name: "Елена, HR-менеджер", text: "Трудовые договоры на двух языках (Каз/Рус) — это просто спасение!", wish: "Было бы здорово сохранять базу сотрудников." },
];

export default function FeedbackPage() {
  const { t } = useLang();
  const [sent, setSent] = useState(false);

  return (
    <div className="min-h-screen px-6 py-10 page-transition max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold text-foreground mb-8 animate-fade-in">{t.feedbackTitle}</h2>

      <div className="space-y-4 mb-10">
        {reviews.map((r, i) => (
          <div key={i} className="glass-card p-5 animate-fade-in" style={{ animationDelay: `${i * 0.1}s` }}>
            <div className="flex items-center gap-2 mb-2">
              <span className="text-sm font-semibold text-foreground">👤 {r.name}</span>
              <div className="flex gap-0.5">{[...Array(5)].map((_, j) => <Star key={j} className="w-3 h-3 fill-primary text-primary" />)}</div>
            </div>
            <p className="text-sm text-muted-foreground">{r.text}</p>
            <p className="text-xs text-primary/70 mt-2">💡 {r.wish}</p>
          </div>
        ))}
      </div>

      <div className="glass-card p-6 animate-fade-in" style={{ animationDelay: "0.2s" }}>
        <p className="text-sm font-semibold text-foreground mb-4">Оставить отзыв:</p>
        {sent ? (
          <p className="text-primary text-sm font-medium">✅ {t.thanks}</p>
        ) : (
          <form onSubmit={(e) => { e.preventDefault(); setSent(true); }} className="space-y-3">
            <input className="w-full bg-secondary/60 text-foreground text-sm rounded-xl px-4 py-3 border border-border/50 focus:outline-none focus:ring-2 focus:ring-primary/40 placeholder:text-muted-foreground/60" placeholder={t.name} required />
            <textarea className="w-full bg-secondary/60 text-foreground text-sm rounded-xl px-4 py-3 border border-border/50 focus:outline-none focus:ring-2 focus:ring-primary/40 min-h-[80px] resize-none placeholder:text-muted-foreground/60" placeholder={t.review} required />
            <button type="submit" className="bg-primary text-primary-foreground px-6 py-3 rounded-xl font-semibold text-sm hover:brightness-110 transition-all">
              {t.send}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}


============================================================
📄 src/pages/AuthorsPage.tsx
============================================================
import { useLang } from "@/lib/LangContext";
import { Code2, MapPin } from "lucide-react";

export default function AuthorsPage() {
  const { t } = useLang();

  return (
    <div className="min-h-screen flex items-center justify-center px-6 page-transition">
      <div className="glass-card p-10 text-center max-w-sm animate-fade-in">
        <div className="w-16 h-16 rounded-2xl bg-primary/15 flex items-center justify-center mx-auto mb-5">
          <Code2 className="w-8 h-8 text-primary" />
        </div>
        <h2 className="text-xl font-bold text-foreground mb-1">{t.authors}</h2>
        <p className="text-lg font-semibold text-foreground mt-4">Yeraly & Ramazan</p>
        <p className="text-sm text-muted-foreground">8 класс</p>
        <div className="flex items-center justify-center gap-1 mt-3 text-muted-foreground text-sm">
          <MapPin className="w-3 h-3" /> Астана
        </div>
      </div>
    </div>
  );
}


============================================================
📄 src/pages/NotFound.tsx
============================================================
import { useLocation } from "react-router-dom";
import { useEffect } from "react";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error("404 Error: User attempted to access non-existent route:", location.pathname);
  }, [location.pathname]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-muted">
      <div className="text-center">
        <h1 className="mb-4 text-4xl font-bold">404</h1>
        <p className="mb-4 text-xl text-muted-foreground">Oops! Page not found</p>
        <a href="/" className="text-primary underline hover:text-primary/90">
          Return to Home
        </a>
      </div>
    </div>
  );
};

export default NotFound;


============================================================
📄 index.html
============================================================
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <!-- TODO: Set the document title to the name of your application -->
    <title>Lovable App</title>
    <meta name="description" content="Lovable Generated Project" />
    <meta name="author" content="Lovable" />

    <!-- TODO: Update og:title to match your application name -->
    <meta property="og:title" content="Lovable App" />
    <meta property="og:description" content="Lovable Generated Project" />
    <meta property="og:type" content="website" />
    <meta property="og:image" content="https://lovable.dev/opengraph-image-p98pqg.png" />

    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@Lovable" />
    <meta name="twitter:image" content="https://lovable.dev/opengraph-image-p98pqg.png" />
  </head>

  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>