/* global React */
const { useEffect, useRef, useState } = React;

const POSTS = [
  {
    id: 1, cat: "MANTENIMIENTO",
    date: "18 May 2026", read: "4 min",
    title: "Cómo extender la vida útil de un grupo electrógeno en planta",
    excerpt: "Cinco rutinas críticas que reducen averías y prolongan operación entre intervenciones mayores.",
    feature: true,
  },
  {
    id: 2, cat: "FLOTAS B2B",
    date: "10 May 2026", read: "6 min",
    title: "Checklist multimarca para mantenimiento preventivo de camiones",
    excerpt: "Lo que separa una flota productiva de una flota detenida en el patio.",
  },
  {
    id: 3, cat: "DIAGNÓSTICO",
    date: "28 Abr 2026", read: "3 min",
    title: "P0420 explicado: cuándo el catalizador realmente falla",
    excerpt: "Cuándo el código OBD-II indica catalizador, y cuándo es sólo un sensor.",
  },
  {
    id: 4, cat: "INDUSTRIAL",
    date: "21 Abr 2026", read: "5 min",
    title: "Montacargas eléctricos vs combustión: cómo elegir",
    excerpt: "Costos por hora, ciclos de trabajo y requisitos de mantenimiento.",
  },
];

function News() {
  return (
    <section id="noticias" className="section">
      <div className="container">
        <div className="sec-head" style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: 32,
          alignItems: "end",
          marginBottom: 48,
        }}>
          <div>
            <div className="eyebrow"><span className="dot"></span>Noticias & mantenimiento</div>
            <h2 style={{
              fontFamily: "var(--font-display)",
              fontWeight: 800,
              fontSize: "clamp(36px, 4.5vw, 64px)",
              lineHeight: 1.02,
              letterSpacing: "-0.03em",
              margin: "16px 0 0",
              textWrap: "balance",
              color: "var(--fg-1)",
            }}>
              Guías y novedades<br/>del taller.
            </h2>
          </div>
          <a href="#" className="btn btn-ghost" style={{ justifySelf: "end" }}>
            Ver todas las publicaciones
            <i data-lucide="arrow-up-right" width="14" height="14" {...{"stroke-width":"2.2"}}></i>
          </a>
        </div>

        <div className="news-grid" style={{
          display: "grid",
          gridTemplateColumns: "1.4fr 1fr",
          gap: 14,
        }}>
          <FeaturePost post={POSTS[0]} />
          <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
            {POSTS.slice(1).map(p => <ListPost key={p.id} post={p} />)}
          </div>
        </div>

        <style>{`
          @media (max-width: 900px) {
            .news-grid { grid-template-columns: 1fr !important; }
            #noticias .sec-head { grid-template-columns: 1fr !important; }
            #noticias .sec-head .btn { justify-self: start !important; }
          }
        `}</style>
      </div>
    </section>
  );
}

function useInView() {
  const ref = useRef(null);
  const [inView, setInView] = useState(false);
  useEffect(() => {
    if (!ref.current) return;
    const io = new IntersectionObserver(([e]) => {
      if (e.isIntersecting) { setInView(true); io.disconnect(); }
    }, { threshold: 0.15 });
    io.observe(ref.current);
    return () => io.disconnect();
  }, []);
  return [ref, inView];
}

function FeaturePost({ post }) {
  const [ref, inView] = useInView();
  const [hover, setHover] = useState(false);
  return (
    <article
      ref={ref}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      className={`reveal ${inView ? "in" : ""}`}
      style={{
        background: "var(--paper-elevated)",
        border: "1px solid rgba(14,16,20,0.05)",
        borderRadius: 28,
        overflow: "hidden",
        boxShadow: hover ? "var(--shadow-2)" : "var(--shadow-soft)",
        transition: "box-shadow var(--dur-base) var(--ease-out), transform var(--dur-base) var(--ease-out)",
        transform: hover ? "translateY(-2px)" : "translateY(0)",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <div className="photo" style={{
        aspectRatio: "16/10",
        borderRadius: 0,
        position: "relative",
      }}>
        <span className="photo-label">FEATURE · HERO PHOTO</span>
        <div style={{
          position: "absolute", top: 18, left: 18,
          padding: "6px 14px",
          borderRadius: 999,
          background: "rgba(14,16,20,0.85)",
          backdropFilter: "blur(12px)",
          color: "var(--paper)",
          fontFamily: "var(--font-body)",
          fontWeight: 700, fontSize: 11,
          letterSpacing: "0.18em",
        }}>{post.cat}</div>
      </div>
      <div style={{ padding: "32px 32px 36px", display: "flex", flexDirection: "column", gap: 14 }}>
        <div style={{
          display: "flex", gap: 12,
          fontFamily: "var(--font-mono)", fontSize: 12, color: "var(--fg-3)",
        }}>
          <span>{post.date}</span><span>·</span><span>{post.read} de lectura</span>
        </div>
        <h3 style={{
          fontFamily: "var(--font-display)",
          fontWeight: 800,
          fontSize: "clamp(24px, 2.6vw, 36px)",
          lineHeight: 1.08,
          letterSpacing: "-0.025em",
          margin: 0,
          textWrap: "balance",
          color: "var(--fg-1)",
        }}>{post.title}</h3>
        <p style={{
          fontFamily: "var(--font-body)",
          fontSize: 15, lineHeight: 1.55,
          color: "var(--fg-2)",
          margin: 0,
          textWrap: "pretty",
        }}>{post.excerpt}</p>
        <a href="#" className="btn btn-primary" style={{ alignSelf: "flex-start", marginTop: 8 }}>
          Leer artículo
          <i data-lucide="arrow-up-right" width="14" height="14" {...{"stroke-width":"2.2"}}></i>
        </a>
      </div>
    </article>
  );
}

function ListPost({ post }) {
  const [ref, inView] = useInView();
  const [hover, setHover] = useState(false);
  return (
    <a
      ref={ref}
      href="#"
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      className={`reveal ${inView ? "in" : ""}`}
      style={{
        display: "grid",
        gridTemplateColumns: "100px 1fr auto",
        gap: 16,
        alignItems: "center",
        background: "var(--paper-elevated)",
        border: "1px solid rgba(14,16,20,0.05)",
        borderRadius: 22,
        padding: 16,
        textDecoration: "none",
        color: "inherit",
        boxShadow: hover ? "var(--shadow-2)" : "var(--shadow-soft)",
        transition: "box-shadow var(--dur-base) var(--ease-out), transform var(--dur-base) var(--ease-out)",
        transform: hover ? "translateX(2px)" : "translateX(0)",
        flex: 1,
      }}
    >
      <div className="photo" style={{ aspectRatio: "1/1", borderRadius: 14 }}></div>
      <div style={{ display: "flex", flexDirection: "column", gap: 4, minWidth: 0 }}>
        <div style={{
          fontFamily: "var(--font-body)",
          fontWeight: 700, fontSize: 10,
          letterSpacing: "0.22em", color: "var(--accent)",
        }}>{post.cat}</div>
        <h4 style={{
          fontFamily: "var(--font-display)",
          fontWeight: 700, fontSize: 18,
          lineHeight: 1.15, letterSpacing: "-0.015em",
          margin: 0, textWrap: "balance",
          color: "var(--fg-1)",
        }}>{post.title}</h4>
        <div style={{
          marginTop: 4,
          fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--fg-3)",
        }}>{post.date} · {post.read}</div>
      </div>
      <div style={{
        width: 40, height: 40,
        borderRadius: "50%",
        background: hover ? "var(--ink)" : "rgba(14,16,20,0.06)",
        color: hover ? "var(--paper)" : "var(--fg-1)",
        display: "flex", alignItems: "center", justifyContent: "center",
        transition: "background var(--dur-fast) var(--ease-out), color var(--dur-fast) var(--ease-out)",
        flexShrink: 0,
      }}>
        <i data-lucide="arrow-up-right" width="18" height="18" {...{"stroke-width":"2"}}></i>
      </div>
    </a>
  );
}

window.News = News;
