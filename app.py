import streamlit as st
import datetime

def calcular_pontuacao(respostas):
    # Pontuação para condicionamento físico
    pontos_condicionamento = {
        "Sedentário (não pratico atividades físicas)": 0,
        "Iniciante (pratico exercícios esporadicamente)": 2,
        "Intermediário (pratico exercícios regularmente)": 4,
        "Avançado (pratico exercícios intensamente)": 6
    }
    
    # Pontuação para experiência com corrida
    pontos_experiencia = {
        "Nunca corri": 0,
        "Corro ocasionalmente (1-2 vezes por mês)": 2,
        "Corro regularmente (1-2 vezes por semana)": 4,
        "Corro frequentemente (3+ vezes por semana)": 6
    }
    
    # Pontuação para idade
    pontos_idade = {
        "18-25 anos": 4,
        "26-35 anos": 3,
        "36-45 anos": 2,
        "46+ anos": 2
    }
    
    # Pontuação para disponibilidade
    pontos_disponibilidade = {
        "2 dias": 1,
        "3 dias": 2,
        "4 dias": 3,
        "5+ dias": 4
    }
    
    # Pontuação para distância atual
    pontos_distancia = {
        "Menos de 1km": 0,
        "1-3km": 2,
        "3-5km": 4,
        "Mais de 5km": 6
    }
    
    pontuacao_base = (
        pontos_condicionamento[respostas['condicionamento']] +
        pontos_experiencia[respostas['experiencia']] +
        pontos_idade[respostas['idade']] +
        pontos_disponibilidade[respostas['disponibilidade']] +
        pontos_distancia[respostas['distancia_atual']]
    )
    
    # Ajustes baseados em limitações físicas
    if respostas['limitacao'] != "Não":
        pontuacao_base = max(0, pontuacao_base - 4)  # Reduz 4 pontos se houver limitação
        
    return pontuacao_base

def verificar_incompatibilidades(respostas, nivel):
    alertas = []
    
    # Verificar prazo vs. objetivo
    if (respostas['objetivo_distancia'] == "21km (meia maratona)" and 
        respostas['prazo'] == "3 meses" and 
        nivel == "Iniciante"):
        alertas.append("⚠️ O prazo de 3 meses pode ser muito curto para preparar uma meia maratona no seu nível atual.")
    
    # Verificar limitações vs. objetivo
    if respostas['limitacao'] != "Não":
        alertas.append("⚠️ Suas limitações físicas requerem atenção especial. Consulte um médico antes de iniciar o programa.")
    
    # Verificar disponibilidade vs. objetivo
    if (respostas['disponibilidade'] == "2 dias" and 
        respostas['objetivo_distancia'] in ["15km", "21km (meia maratona)"]):
        alertas.append("⚠️ A frequência de treino pode ser insuficiente para seu objetivo de distância.")
    
    return alertas

def gerar_plano_treino(nivel, respostas):
    plano_base = {
        "Iniciante": {
            "freq_semanal": 3,
            "estrutura_base": """
            **Estrutura Semanal:**
            - Treino 1: Corrida/Caminhada intervalada
            - Treino 2: Fortalecimento e técnica
            - Treino 3: Corrida contínua leve
            
            **Progressão:**
            - Semanas 1-4: 
              * Alternar 2 min corrida / 2 min caminhada (20 min total)
            - Semanas 5-8: 
              * Alternar 3 min corrida / 1 min caminhada (25 min total)
            - Semanas 9-12: 
              * Corrida contínua leve (20-30 min)
            """,
            "aquecimento": "10 min de caminhada + exercícios de mobilidade",
            "volta_calma": "5 min de caminhada leve + alongamento"
        },
        "Intermediário": {
            "freq_semanal": 4,
            "estrutura_base": """
            **Estrutura Semanal:**
            - Treino 1: Intervalado curto
            - Treino 2: Corrida contínua moderada
            - Treino 3: Fortalecimento específico
            - Treino 4: Corrida longa leve
            
            **Progressão:**
            - Semanas 1-4: 
              * Intervalado: 6-8x (1 min forte / 1 min leve)
              * Corrida contínua: 30-40 min
              * Corrida longa: 45-60 min
            - Semanas 5-8:
              * Intervalado: 8-10x (1 min forte / 1 min leve)
              * Corrida contínua: 40-50 min
              * Corrida longa: 60-75 min
            """,
            "aquecimento": "15 min de corrida leve + exercícios de técnica",
            "volta_calma": "10 min de corrida muito leve + alongamento"
        },
        "Avançado": {
            "freq_semanal": 5,
            "estrutura_base": """
            **Estrutura Semanal:**
            - Treino 1: Intervalado de alta intensidade
            - Treino 2: Corrida contínua moderada
            - Treino 3: Treino de força e potência
            - Treino 4: Corrida técnica e ritmo
            - Treino 5: Corrida longa progressiva
            
            **Progressão:**
            - Semanas 1-4:
              * Intervalado: 10-12x (1 min forte / 1 min leve)
              * Corridas moderadas: 50-60 min
              * Corrida longa: 90-120 min
            - Semanas 5-8:
              * Intervalado: 12-15x (1 min forte / 1 min leve)
              * Corridas moderadas: 60-75 min
              * Corrida longa: 120-150 min
            """,
            "aquecimento": "20 min de corrida progressiva + exercícios de técnica",
            "volta_calma": "15 min de corrida leve + alongamento dinâmico"
        }
    }
    
    # Ajustes baseados nas preferências e limitações
    plano = plano_base[nivel]
    recomendacoes = []
    
    # Ajuste por período do dia
    if respostas['periodo'] != "Flexível":
        recomendacoes.append(f"Programe seus treinos para o período da {respostas['periodo'].lower()}, respeitando seu horário de preferência.")
    
    # Ajuste por limitação física
    if respostas['limitacao'] != "Não":
        recomendacoes.append("Inclua sessões extras de fortalecimento e mobilidade. Monitore eventuais dores ou desconfortos.")
    
    # Ajuste por meta
    if respostas['meta'] == "Perder peso":
        recomendacoes.append("Mantenha os treinos na zona aeróbia (consiga manter uma conversa) e combine com alimentação adequada.")
    elif respostas['meta'] == "Melhorar tempo/performance":
        recomendacoes.append("Foque nos treinos intervalados e inclua exercícios de força específicos para corrida.")
    
    return plano, recomendacoes

def main():
    st.title("Avaliação Avançada para Corrida de Rua")
    st.write("Complete o questionário abaixo para receber seu plano personalizado de treino.")
    
    with st.form("questionario_corrida"):
        # Questões básicas
        condicionamento = st.radio(
            "Qual seu nível atual de condicionamento físico?",
            ["Sedentário (não pratico atividades físicas)", 
             "Iniciante (pratico exercícios esporadicamente)",
             "Intermediário (pratico exercícios regularmente)",
             "Avançado (pratico exercícios intensamente)"]
        )
        
        experiencia = st.radio(
            "Qual sua experiência prévia com corrida?",
            ["Nunca corri",
             "Corro ocasionalmente (1-2 vezes por mês)",
             "Corro regularmente (1-2 vezes por semana)",
             "Corro frequentemente (3+ vezes por semana)"]
        )
        
        idade = st.radio(
            "Qual sua idade?",
            ["18-25 anos", "26-35 anos", "36-45 anos", "46+ anos"]
        )
        
        # Questões adicionais
        disponibilidade = st.radio(
            "Quantos dias por semana você tem disponível para treinar?",
            ["2 dias", "3 dias", "4 dias", "5+ dias"]
        )
        
        meta = st.radio(
            "Qual sua meta principal com a corrida?",
            ["Melhorar condicionamento físico", "Perder peso",
             "Participar de provas", "Melhorar tempo/performance"]
        )
        
        distancia_atual = st.radio(
            "Qual distância você consegue correr atualmente sem parar?",
            ["Menos de 1km", "1-3km", "3-5km", "Mais de 5km"]
        )
        
        limitacao = st.radio(
            "Possui alguma limitação física ou condição médica?",
            ["Não", "Sim, problemas articulares",
             "Sim, problemas cardíacos", "Sim, outros"]
        )
        
        if limitacao == "Sim, outros":
            limitacao_especifica = st.text_input("Especifique sua limitação:")
        
        objetivo_distancia = st.radio(
            "Qual seu objetivo de distância nas provas?",
            ["5km", "10km", "15km", "21km (meia maratona)"]
        )
        
        prazo = st.radio(
            "Em quanto tempo pretende atingir seu objetivo?",
            ["3 meses", "6 meses", "9 meses", "12 meses"]
        )
        
        periodo = st.radio(
            "Prefere treinar em qual período do dia?",
            ["Manhã", "Tarde", "Noite", "Flexível"]
        )
        
        submitted = st.form_submit_button("Gerar Plano de Treino")
        
    if submitted:
        # Coletar todas as respostas
        respostas = {
            'condicionamento': condicionamento,
            'experiencia': experiencia,
            'idade': idade,
            'disponibilidade': disponibilidade,
            'meta': meta,
            'distancia_atual': distancia_atual,
            'limitacao': limitacao,
            'objetivo_distancia': objetivo_distancia,
            'prazo': prazo,
            'periodo': periodo
        }
        
        # Calcular pontuação e determinar nível
        pontuacao = calcular_pontuacao(respostas)
        
        if pontuacao <= 9:
            nivel = "Iniciante"
        elif pontuacao <= 19:
            nivel = "Intermediário"
        else:
            nivel = "Avançado"
            
        # Exibir resultados
        st.write("---")
        st.subheader("Resultado da Avaliação")
        st.write(f"**Pontuação total:** {pontuacao} pontos")
        st.write(f"**Nível classificado:** {nivel}")
        
        # Verificar e exibir alertas
        alertas = verificar_incompatibilidades(respostas, nivel)
        if alertas:
            st.write("**Alertas importantes:**")
            for alerta in alertas:
                st.warning(alerta)
        
        # Gerar e exibir plano
        plano, recomendacoes = gerar_plano_treino(nivel, respostas)
        
        st.write("---")
        st.subheader("Seu Plano de Treino Personalizado")
        st.write(f"**Frequência semanal recomendada:** {plano['freq_semanal']} treinos por semana")
        
        st.write("**Estrutura dos Treinos:**")
        st.markdown(plano['estrutura_base'])
        
        st.write("**Aquecimento:**")
        st.write(plano['aquecimento'])
        
        st.write("**Volta à calma:**")
        st.write(plano['volta_calma'])
        
        if recomendacoes:
            st.write("**Recomendações Específicas:**")
            for rec in recomendacoes:
                st.info(rec)
        
        # Adicionar data de geração do plano
        st.write("---")
        st.write(f"Plano gerado em: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")

if __name__ == "__main__":
    main()