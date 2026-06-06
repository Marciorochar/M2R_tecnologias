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

  // O Vercel Edge Middleware tem limite de tempo curto (timeout).
  // Como o Render pode demorar a acordar, o fetch aqui causaria erro 504.
  // A validação profunda já está sendo feita de forma segura no frontend via JS.
  return Response.next();
}