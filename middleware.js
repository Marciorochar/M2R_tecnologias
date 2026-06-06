// Configuração das rotas que o middleware vai interceptar
export const config = {
  matcher: [
    '/Login/Site/:path*', // Protege todos os arquivos dentro de Login/Site/
  ],
};

export default async function middleware(request) {
  const url = new URL(request.url);
  
  // Obtém os cookies enviados pelo navegador na requisição
  const cookieHeader = request.headers.get('cookie') || '';
  
  // Extrai o valor exato do token m2r_token
  const tokenMatch = cookieHeader.match(/m2r_token=([^;]+)/);
  const token = tokenMatch ? tokenMatch[1] : null;

  // Se não houver token, redireciona para a página de login imediatamente
  if (!token) {
    url.pathname = '/login.html';
    return Response.redirect(url);
  }

  // Validação Criptográfica: Pergunta ao backend se o token é real/válido
  try {
    const verifyRes = await fetch("https://m2r-backend.onrender.com/verify", {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    // Se o backend retornar erro (ex: 401 Unauthorized), o token é falso, adulterado ou expirou
    if (!verifyRes.ok) {
      url.pathname = '/login.html';
      return Response.redirect(url);
    }
  } catch (error) {
    // Se houver erro de rede com o backend, bloqueamos o acesso por segurança
    url.pathname = '/login.html';
    return Response.redirect(url);
  }
  // O Vercel Edge Middleware tem limite de tempo curto (timeout).
  // Como o Render pode demorar a acordar, o fetch aqui causaria erro 504.
  // A validação profunda já está sendo feita de forma segura no frontend via JS.
  return Response.next();
  
  // Comando nativo do Vercel para permitir que o site continue carregando a página
  return new Response(null, {
    headers: { 'x-middleware-next': '1' }
  });
}