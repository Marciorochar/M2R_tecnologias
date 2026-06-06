// Configuração das rotas que o middleware vai interceptar
export const config = {
  matcher: [
    '/Login/Site/:path*', // Protege todos os arquivos dentro de Login/Site/
  ],
};

export default function middleware(request) {
  const url = new URL(request.url);
  
  // Obtém os cookies enviados pelo navegador na requisição
  const cookieHeader = request.headers.get('cookie') || '';
  
  // Verifica se o nosso cookie de autenticação existe
  const hasToken = cookieHeader.includes('m2r_token=');

  // Se tentar acessar a área restrita sem o token, redireciona para a página de login
  if (!hasToken) {
    url.pathname = '/login.html';
    return Response.redirect(url);
  }
}