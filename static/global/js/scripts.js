function my_scope() {
  document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.exclude-button');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); // Evita a ação padrão do link

            const confirmation = confirm('Tem certeza de que deseja excluir esta receita?');

            if (confirmation) {
                // Se confirmado, redirecionar para a URL de exclusão
                const link = this.querySelector('a').getAttribute('href');
                window.location.href = link;
            }
        });
    });
});
}
  my_scope();