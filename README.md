# Payment Transfer Challenge

Part of the [Programming Lab](https://github.com/ViniciusRibeiroo/programming-lab).

A REST API for money transfers between users and merchants, inspired by a public backend engineering challenge, https://github.com/PicPay/picpay-desafio-backend.

## 🎯 Objective

Build a money transfer API that applies the required business rules, maintains transaction consistency, and integrates with external authorization and notification services.

The project is also used to practice the complete greenfield development process, including domain modeling, architecture, implementation, testing, persistence, integrations, and documentation.

## 📋 Requirements

The system supports two types of accounts:

* **Users** — can send and receive money.
* **Merchants** — can receive money but cannot send transfers.

Each account has:

* Full name
* CPF/CNPJ
* E-mail
* Password
* Balance

CPF/CNPJ and e-mail must be unique.

### Transfer

A transfer must:

1. Validate the payer and payee.
2. Ensure the payer has sufficient balance.
3. Check whether the payer is allowed to transfer.
4. Request authorization from an external service.
5. Debit the payer.
6. Credit the payee.
7. Execute the balance changes transactionally.
8. Notify the payee after a successful transfer.

### Main endpoint

```http
POST /transfer
Content-Type: application/json
```

```json
{
  "value": 100.0,
  "payer": 4,
  "payee": 15
}
```

## 🔌 External Services

### Authorization

Used to authorize transfers before they are completed.

```http
GET https://util.devi.tools/api/v2/authorize
```

### Notification

Used to notify the payee after a successful transfer.

```http
POST https://util.devi.tools/api/v1/notify
```

External integrations should remain isolated from the core business logic.

## 🚫 Out of Scope

The initial implementation does not include:

* Frontend
* API authentication
* User registration
* Administrative interface

Users and merchants can be created through development or test mechanisms.

## 🧩 Multiple Implementations

The same problem will be implemented using different stacks to compare approaches and gain experience across ecosystems.

```text
python/   → Python + FastAPI
dotnet/   → C# + .NET
node/     → Node.js + TypeScript
```

Each implementation has its own README covering its specific:

* Stack
* Architecture
* Setup
* Project structure
* Execution
* Tests
* Endpoints
* Technical decisions

## 🏗️ Architecture

Architecture and technical decisions will be documented during development.

Technologies and patterns should be introduced only when they provide a clear benefit to the problem being solved.

## 📚 Learnings

Each implementation will document relevant:

* Problems encountered
* Technical decisions
* Approaches considered and rejected
* Lessons learned
* Improvements for future iterations

## 🚀 Possible Future Improvements

Potential improvements outside the initial scope:

* Caching
* Asynchronous processing
* Messaging
* Advanced observability
* Integration resilience
* Scalability
* Alternative persistence strategies

