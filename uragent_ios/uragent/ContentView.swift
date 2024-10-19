//
//  ContentView.swift
//  uragent
//
//  Created by Abhishyant Khare on 10/16/24.
//

import SwiftUI
import AuthenticationServices

struct ContentView: View {
    @State private var showAlert = false
    @State private var alertMessage = ""

    var body: some View {
        VStack {
            Text("UrAgent").padding(.vertical, 50)
            SignInWithAppleButton(.signIn) { request in
                request.requestedScopes = [.fullName, .email]
            } onCompletion: { result in
                switch result {
                case .success(let authorization):
                    if let appleIDCredential = authorization.credential as? ASAuthorizationAppleIDCredential {
                        let email = appleIDCredential.email ?? ""
                        let fullName = appleIDCredential.fullName?.givenName ?? ""
                        let id = appleIDCredential.user
                        sendUserDataToServer(email: email, name: fullName, id: id)
                    }
                case .failure(let error):
                    alertMessage = "Could not authenticate: \(error.localizedDescription)"
                    showAlert = true
                }
            }
            .frame(height: 50)
            .padding(.horizontal, 50)
        }
        .padding()
        .alert(isPresented: $showAlert) {
            Alert(title: Text("Sign In Result"), message: Text(alertMessage), dismissButton: .default(Text("OK")))
        }
    }<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>
    
    func sendUserDataToServer(email: String, name: String, id: String) {
        guard let url = URL(string: "http://localhost:8000/users") 
        
        let body: [String: String] = ["email": email, "name": name]
        let jsonData = try? JSONSerialization.data(withJSONObject: body)
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = jsonData
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            DispatchQueue.main.async {
                if let error = error {
                    alertMessage = "Error: \(error.localizedDescription)"
                    showAlert = true
                    return
                }
                
                guard let httpResponse = response as? HTTPURLResponse else {
                    alertMessage = "Invalid response"
                    showAlert = true
                    return
                }
                
                if (200...299).contains(httpResponse.statusCode) {
                    alertMessage = "User data sent successfully"
                } else {
                    alertMessage = "Server error: \(httpResponse.statusCode)"
                }
                showAlert = true
            }
        }.resume()
    }
}

#Preview {
    ContentView()
}
